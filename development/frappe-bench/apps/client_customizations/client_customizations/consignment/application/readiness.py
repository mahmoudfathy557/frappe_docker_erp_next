import importlib

from client_customizations.consignment.infrastructure.frappe_adapter import db_get_value


STATUS_PASS = "PASS"
STATUS_WARN = "WARN"
STATUS_FAIL = "FAIL"

REQUIRED_CONSIGNMENT_DOCTYPES = (
	"Consignment Agreement",
	"Consignment Agreement Item",
	"Consignment Settlement",
	"Consignment Settlement Item",
)

REQUIRED_CUSTOM_FIELDS = (
	"Purchase Receipt-custom_is_consignment",
	"Purchase Receipt Item-custom_is_consignment",
	"Purchase Receipt Item-custom_consignment_supplier",
	"Delivery Note-custom_is_consignment",
	"Delivery Note-custom_consignment_supplier",
	"Delivery Note Item-custom_is_consignment",
	"Delivery Note Item-custom_consignment_supplier",
	"Delivery Note Item-custom_consignment_settlement",
	"Sales Invoice-custom_is_consignment",
	"Sales Invoice-custom_consignment_supplier",
	"Sales Invoice Item-custom_is_consignment",
	"Sales Invoice Item-custom_consignment_supplier",
	"Sales Invoice Item-custom_consignment_settlement",
	"Purchase Invoice-custom_consignment_settlement",
)

EXPECTED_DOC_EVENT_HOOKS = {
	"Purchase Receipt": {
		"before_save": "client_customizations.consignment.validations.validate_purchase_receipt_for_consignment",
	},
	"Delivery Note": {
		"on_submit": "client_customizations.consignment.validations.validate_sale_posting_for_consignment",
		"on_cancel": "client_customizations.consignment.validations.validate_sale_cancel_not_linked_to_submitted_settlement",
	},
	"Sales Invoice": {
		"on_submit": "client_customizations.consignment.validations.validate_sale_posting_for_consignment",
		"on_cancel": "client_customizations.consignment.validations.validate_sale_cancel_not_linked_to_submitted_settlement",
	},
}

EXPECTED_SCHEDULER_HOOKS = {
	"daily": (
		"client_customizations.consignment.jobs.generate_daily_draft_settlements",
	),
}

_STATUS_PRIORITY = {
	STATUS_PASS: 0,
	STATUS_WARN: 1,
	STATUS_FAIL: 2,
}


def _missing_required_items(required_items, existing_items):
	required = set(required_items or [])
	existing = set(existing_items or [])
	return sorted(required - existing)


def make_check_result(name, status, details, missing_items=None):
	result = {
		"name": name,
		"status": status,
		"details": details,
	}
	if missing_items is not None:
		result["missing_items"] = list(missing_items)
	return result


def aggregate_overall_status(checks):
	highest_priority = _STATUS_PRIORITY[STATUS_PASS]
	for check in checks or []:
		status = check.get("status", STATUS_PASS)
		priority = _STATUS_PRIORITY.get(status, _STATUS_PRIORITY[STATUS_FAIL])
		if priority > highest_priority:
			highest_priority = priority

	for status, priority in _STATUS_PRIORITY.items():
		if priority == highest_priority:
			return status
	return STATUS_FAIL


def _find_missing_doc_event_bindings(expected_hooks, actual_hooks):
	missing = []
	actual_doc_events = actual_hooks or {}

	for doctype in sorted(expected_hooks):
		expected_events = expected_hooks.get(doctype, {})
		actual_events = actual_doc_events.get(doctype) or {}
		for event_name in sorted(expected_events):
			expected_handler = expected_events[event_name]
			if actual_events.get(event_name) != expected_handler:
				missing.append(f"{doctype}.{event_name}:{expected_handler}")

	return missing


def _find_missing_scheduler_bindings(expected_hooks, actual_hooks):
	missing = []
	actual_scheduler = actual_hooks or {}

	for frequency in sorted(expected_hooks):
		expected_handlers = expected_hooks.get(frequency, ())
		actual_handlers = tuple(actual_scheduler.get(frequency) or ())
		for expected_handler in expected_handlers:
			if expected_handler not in actual_handlers:
				missing.append(f"{frequency}:{expected_handler}")

	return missing


def build_readiness_payload(existing_doctypes, existing_custom_fields, actual_doc_events, actual_scheduler_events):
	checks = []

	missing_doctypes = _missing_required_items(REQUIRED_CONSIGNMENT_DOCTYPES, existing_doctypes)
	checks.append(
		make_check_result(
			name="required_doctypes",
			status=STATUS_FAIL if missing_doctypes else STATUS_PASS,
			details="Consignment custom DocType presence",
			missing_items=missing_doctypes,
		)
	)

	missing_custom_fields = _missing_required_items(REQUIRED_CUSTOM_FIELDS, existing_custom_fields)
	checks.append(
		make_check_result(
			name="required_custom_fields",
			status=STATUS_FAIL if missing_custom_fields else STATUS_PASS,
			details="Consignment custom field presence",
			missing_items=missing_custom_fields,
		)
	)

	missing_doc_event_hooks = _find_missing_doc_event_bindings(EXPECTED_DOC_EVENT_HOOKS, actual_doc_events)
	checks.append(
		make_check_result(
			name="doc_event_hooks",
			status=STATUS_FAIL if missing_doc_event_hooks else STATUS_PASS,
			details="Configured doc_events hooks match expected consignment handlers",
			missing_items=missing_doc_event_hooks,
		)
	)

	missing_scheduler_hooks = _find_missing_scheduler_bindings(EXPECTED_SCHEDULER_HOOKS, actual_scheduler_events)
	checks.append(
		make_check_result(
			name="scheduler_hooks",
			status=STATUS_FAIL if missing_scheduler_hooks else STATUS_PASS,
			details="Configured scheduler_events hooks include expected consignment jobs",
			missing_items=missing_scheduler_hooks,
		)
	)

	return {
		"overall_status": aggregate_overall_status(checks),
		"checks": checks,
	}


def _collect_existing_by_name(doctype_name, names):
	existing = []
	for name in names:
		if db_get_value(doctype_name, name, "name"):
			existing.append(name)
	return existing


def run_consignment_readiness_healthcheck():
	"""Bench execute entrypoint for deployment-readiness checks."""
	hooks_module = importlib.import_module("client_customizations.hooks")

	existing_doctypes = _collect_existing_by_name("DocType", REQUIRED_CONSIGNMENT_DOCTYPES)
	existing_custom_fields = _collect_existing_by_name("Custom Field", REQUIRED_CUSTOM_FIELDS)
	actual_doc_events = getattr(hooks_module, "doc_events", {})
	actual_scheduler_events = getattr(hooks_module, "scheduler_events", {})

	return build_readiness_payload(
		existing_doctypes=existing_doctypes,
		existing_custom_fields=existing_custom_fields,
		actual_doc_events=actual_doc_events,
		actual_scheduler_events=actual_scheduler_events,
	)
