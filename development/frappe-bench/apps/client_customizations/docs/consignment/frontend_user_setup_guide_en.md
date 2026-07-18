# Frontend User Setup Guide (English)

Status: End-user guide for first-time frontend setup in ERPNext  
Audience: Business users (non-technical)

## 1. Purpose and Who Should Use This Guide

This guide helps daily users configure their ERPNext screen after first login, so they can work faster with fewer mistakes. Use this if you work in purchasing, sales, warehouse, or finance operations.

## 2. Before You Start (Required Info)

Prepare this information before login:
1. Your ERPNext URL.
2. Your username and temporary password.
3. Your company name.
4. Your preferred language (English or Arabic).
5. Your local time zone.
6. Your preferred date format (for example: DD-MM-YYYY).
7. Your preferred number format (for example: 1,234.56).
8. The list of documents you use daily: Purchase Receipt, Delivery Note, Sales Invoice, Consignment Settlement.
9. If you are using this frappe_docker workspace, the frontend opens at http://localhost:8080.
10. If Purchase Receipt is not visible in the menu, use the top search bar or ask your admin to grant Buying access.

## 3. First Login Steps

1. If you are using this workspace locally, open http://localhost:8080.
2. If you are using a deployed environment, open the ERPNext URL given by your admin.
3. Enter your username and password.
4. Click Log In.
5. If prompted, create a new password and click Update Password.
6. Wait for the home screen to load fully.
7. Verify your full name appears in the top-right user menu.

If you cannot see Purchase Receipt after login:

1. Use the top search bar and type Purchase Receipt.
2. If the search returns nothing, ask your admin for Buying permission or the correct role.
3. You can also check the Buying workspace if your role has access.

## 4. Change Language

1. Click your profile icon in the top-right corner.
2. Click My Settings.
3. Find the Language field.
4. Select English or Arabic.
5. Click Save.
6. Refresh the page to confirm all menus appear in your selected language.

## 5. Set User Basics (Time Zone, Date Format, Number Format)

1. Stay in My Settings.
2. Set Time Zone to your local city/region.
3. Set Date Format (recommended: DD-MM-YYYY unless your team requires a different format).
4. Set Number Format to your finance/team standard.
5. Click Save.
6. Open one document (for example Sales Invoice) and confirm date and numbers display correctly.

## 6. Personalize Home/Workspace Shortcuts for Daily Tasks

1. Go to Workspace from the main menu.
2. Open the workspace you use most (for example Selling, Buying, Stock, Accounts).
3. Click the shortcut or star option to pin frequent links.
4. Add quick links for:
   1. Purchase Receipt List
   2. Delivery Note List
   3. Sales Invoice List
   4. Consignment Settlement List
5. Reorder shortcuts so your top 3 daily actions appear first.
6. Save changes.

## 7. Save and Reuse List/Report Filters

Use this same pattern in each list page.

### 7.1 Purchase Receipt

1. Go to Purchase Receipt List.
2. If the menu item is hidden, use the search bar and open Purchase Receipt from there.
3. Click Filter.
4. Add common filters (example: Company, Posting Date, Status).
5. Click Save Filter (or Save as new filter, based on your UI label).
6. Name it clearly, for example: PR - My Daily View.
7. Reopen the list and confirm the saved filter is available.

### 7.2 Delivery Note

1. Go to Delivery Note List.
2. Click Filter.
3. Add filters you use daily (example: Company, Posting Date, Customer).
4. Save the filter as DN - Daily Follow-up.
5. Test by leaving the page and opening it again.

### 7.3 Sales Invoice

1. Go to Sales Invoice List.
2. Click Filter.
3. Add your regular filters (example: Company, Posting Date, Outstanding Amount).
4. Save as SI - Collection Focus.
5. Reuse this filter each morning.

### 7.4 Consignment Settlement

1. Go to Consignment Settlement List.
2. Click Filter.
3. Add key filters (example: Company, Posting Date, Status, Supplier).
4. Save as CS - Daily Draft Check.
5. Reuse for daily review before submission.

## 8. Create Saved Views for Role-Based Work

1. Open the list page related to your role.
2. Apply your role filters.
3. Save the view with a role name:
   1. Warehouse - Today Receipts
   2. Sales - Pending Delivery
   3. Finance - Invoice Review
   4. Consignment - Draft Settlements
4. Set your main view as default if your role allows it.
5. Share naming standards with your team so everyone uses the same labels.

## 9. Notification and Reminder Preferences

1. Click profile icon, then open Notifications or My Settings.
2. Enable only useful alerts (document assignments, mentions, workflow actions).
3. Disable noisy alerts not relevant to your daily role.
4. Check Email Digest or reminder frequency.
5. Save settings.
6. Test by assigning one sample task to yourself and confirming alert delivery.

## 10. Daily Startup Checklist

1. Log in and confirm correct language.
2. Confirm time zone/date/number format on one transaction.
3. Open your saved workspace shortcuts.
4. Apply your saved list filters.
5. Review new assignments and notifications.
6. Start with your priority queue (oldest pending first).

## 11. Troubleshooting Quick Fixes

1. Problem: Menus still show wrong language.
   Fix: Reopen My Settings, reselect language, click Save, then hard refresh browser.
2. Problem: Saved filter not visible.
   Fix: Return to list, reapply filter, save again with a unique name.
3. Problem: Dates or amounts look incorrect.
   Fix: Recheck Date Format and Number Format in My Settings.
4. Problem: Shortcut disappeared.
   Fix: Reopen Workspace and pin the shortcut again.
5. Problem: No notifications.
   Fix: Check notification preferences and browser notification permission.
6. Problem: Local page shows 404 on localhost.
   Fix: Make sure the docker frontend is running on port 8080 and use http://localhost:8080 in the browser.

## 12. Who to Contact (Escalation)

Contact in this order:
1. Your team lead (role/process question).
2. Business process owner (policy or approval rule question).
3. ERP support/helpdesk (system behavior issue, access issue, bug).

When escalating, include:
1. Your username.
2. Screen name and document type.
3. What you clicked.
4. Error message screenshot (if available).
5. Time of issue.

## 13. One-Page Quick Checklist

1. Login successful.
2. Correct language selected.
3. Time zone/date/number format verified.
4. Workspace shortcuts ready.
5. Saved filters loaded:
   1. PR - My Daily View
   2. DN - Daily Follow-up
   3. SI - Collection Focus
   4. CS - Daily Draft Check
6. Notifications enabled for assignments and workflow alerts.
7. Priority tasks started.
8. Issues escalated with screenshot and timestamp.
