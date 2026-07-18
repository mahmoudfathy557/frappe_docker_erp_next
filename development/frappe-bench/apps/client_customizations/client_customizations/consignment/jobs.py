"""Compatibility wrapper for jobs entrypoints.

Runtime logic moved to the interface layer.
"""

from client_customizations.consignment.interface.jobs import (  # noqa: F401
	_select_target_company_names,
	build_company_summary,
	generate_daily_draft_settlements,
)

__all__ = [
	"_select_target_company_names",
	"build_company_summary",
	"generate_daily_draft_settlements",
]
