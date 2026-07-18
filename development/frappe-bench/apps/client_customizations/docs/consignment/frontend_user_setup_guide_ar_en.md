# Frontend User Setup Guide (English + Arabic)

Status: End-user guide for first-time frontend setup in ERPNext  
Audience: Business users (non-technical)

## 1. Purpose and Who Should Use This Guide

### English
This guide helps daily users configure their ERPNext screen after first login, so they can work faster with fewer mistakes. Use this if you work in purchasing, sales, warehouse, or finance operations.

### العربية
يساعد هذا الدليل المستخدمين اليوميين على ضبط واجهة ERPNext بعد أول تسجيل دخول، حتى يعملوا بسرعة أكبر وبأخطاء أقل. استخدم هذا الدليل إذا كنت تعمل في المشتريات أو المبيعات أو المستودعات أو العمليات المالية.

## 2. Before You Start (Required Info)

### English
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

### العربية
جهز هذه المعلومات قبل تسجيل الدخول:
1. رابط ERPNext الخاص بشركتك.
2. اسم المستخدم وكلمة المرور المؤقتة.
3. اسم الشركة.
4. اللغة المفضلة (English أو العربية).
5. المنطقة الزمنية المحلية.
6. تنسيق التاريخ المفضل (مثال: DD-MM-YYYY).
7. تنسيق الأرقام المفضل (مثال: 1,234.56).
8. قائمة المستندات التي تستخدمها يوميا: Purchase Receipt وDelivery Note وSales Invoice وConsignment Settlement.
9. إذا كنت تستخدم هذه البيئة المحلية في frappe_docker، فالواجهة تفتح على http://localhost:8080.
10. إذا لم تظهر Purchase Receipt في القائمة، استخدم شريط البحث أو اطلب من المسؤول تفعيل صلاحية Buying.

## 3. First Login Steps

### English
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

### العربية
1. إذا كنت تستخدم هذه البيئة محليا، افتح http://localhost:8080.
2. إذا كنت تستخدم بيئة من الشركة أو الاستضافة، افتح رابط ERPNext الذي أعطاه لك المسؤول.
3. ادخل اسم المستخدم وكلمة المرور.
4. اضغط Log In.
5. إذا طلب منك النظام، أنشئ كلمة مرور جديدة ثم اضغط Update Password.
6. انتظر حتى تظهر الصفحة الرئيسية بالكامل.
7. تأكد أن اسمك الكامل يظهر في قائمة المستخدم أعلى اليمين.

إذا لم تظهر Purchase Receipt بعد تسجيل الدخول:

1. استخدم شريط البحث في الأعلى واكتب Purchase Receipt.
2. إذا لم تظهر في البحث أيضا، اطلب من المسؤول تفعيل صلاحية Buying أو إعطائك الدور الصحيح.
3. يمكنك أيضا فتح مساحة عمل Buying إذا كانت الصلاحية متاحة لك.

## 4. Change Language

### English
1. Click your profile icon in the top-right corner.
2. Click My Settings.
3. Find the Language field.
4. Select English or Arabic.
5. Click Save.
6. Refresh the page to confirm all menus appear in your selected language.

### العربية
1. اضغط على أيقونة الحساب أعلى اليمين.
2. اضغط My Settings.
3. ابحث عن خانة Language.
4. اختر English أو العربية.
5. اضغط Save.
6. حدث الصفحة للتأكد أن القوائم ظهرت باللغة التي اخترتها.

## 5. Set User Basics (Time Zone, Date Format, Number Format)

### English
1. Stay in My Settings.
2. Set Time Zone to your local city/region.
3. Set Date Format (recommended: DD-MM-YYYY unless your team requires a different format).
4. Set Number Format to your finance/team standard.
5. Click Save.
6. Open one document (for example Sales Invoice) and confirm date and numbers display correctly.

### العربية
1. ابق في صفحة My Settings.
2. اضبط Time Zone حسب مدينتك أو منطقتك.
3. اضبط Date Format (الموصى به: DD-MM-YYYY إلا إذا لدى فريقك تنسيق مختلف).
4. اضبط Number Format حسب معيار فريقك المالي.
5. اضغط Save.
6. افتح مستندا واحدا (مثلا Sales Invoice) وتأكد أن التاريخ والأرقام تظهر بشكل صحيح.

## 6. Personalize Home/Workspace Shortcuts for Daily Tasks

### English
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

### العربية
1. اذهب إلى Workspace من القائمة الرئيسية.
2. افتح مساحة العمل التي تستخدمها غالبا (مثل Selling أو Buying أو Stock أو Accounts).
3. استخدم خيار التثبيت أو النجمة لإضافة الروابط السريعة.
4. أضف روابط سريعة لـ:
   1. Purchase Receipt List
   2. Delivery Note List
   3. Sales Invoice List
   4. Consignment Settlement List
5. أعد ترتيب الاختصارات بحيث تظهر أهم 3 مهام يومية في البداية.
6. احفظ التغييرات.

## 7. Save and Reuse List/Report Filters

### English
Use this same pattern in each list page.

#### 7.1 Purchase Receipt
1. Go to Purchase Receipt List.
2. If the menu item is hidden, use the search bar and open Purchase Receipt from there.
3. Click Filter.
4. Add common filters (example: Company, Posting Date, Status).
5. Click Save Filter (or Save as new filter, based on your UI label).
6. Name it clearly, for example: PR - My Daily View.
7. Reopen the list and confirm the saved filter is available.

#### 7.2 Delivery Note
1. Go to Delivery Note List.
2. Click Filter.
3. Add filters you use daily (example: Company, Posting Date, Customer).
4. Save the filter as DN - Daily Follow-up.
5. Test by leaving the page and opening it again.

#### 7.3 Sales Invoice
1. Go to Sales Invoice List.
2. Click Filter.
3. Add your regular filters (example: Company, Posting Date, Outstanding Amount).
4. Save as SI - Collection Focus.
5. Reuse this filter each morning.

#### 7.4 Consignment Settlement
1. Go to Consignment Settlement List.
2. Click Filter.
3. Add key filters (example: Company, Posting Date, Status, Supplier).
4. Save as CS - Daily Draft Check.
5. Reuse for daily review before submission.

### العربية
استخدم نفس الطريقة التالية في كل صفحة قائمة.

#### 7.1 Purchase Receipt
1. اذهب إلى قائمة Purchase Receipt.
2. إذا كانت القائمة مخفية، استخدم شريط البحث وافتح Purchase Receipt من هناك.
3. اضغط Filter.
4. أضف الفلاتر المتكررة (مثال: Company وPosting Date وStatus).
5. اضغط Save Filter (أو Save as new filter حسب تسمية النظام).
6. اختر اسما واضحا مثل: PR - My Daily View.
7. افتح القائمة مرة أخرى وتأكد أن الفلتر المحفوظ موجود.

#### 7.2 Delivery Note
1. اذهب إلى قائمة Delivery Note.
2. اضغط Filter.
3. أضف الفلاتر اليومية (مثال: Company وPosting Date وCustomer).
4. احفظ الفلتر باسم DN - Daily Follow-up.
5. اختبره بالخروج من الصفحة ثم فتحها مرة أخرى.

#### 7.3 Sales Invoice
1. اذهب إلى قائمة Sales Invoice.
2. اضغط Filter.
3. أضف الفلاتر الأساسية (مثال: Company وPosting Date وOutstanding Amount).
4. احفظ باسم SI - Collection Focus.
5. أعد استخدام هذا الفلتر كل صباح.

#### 7.4 Consignment Settlement
1. اذهب إلى قائمة Consignment Settlement.
2. اضغط Filter.
3. أضف الفلاتر المهمة (مثال: Company وPosting Date وStatus وSupplier).
4. احفظ باسم CS - Daily Draft Check.
5. استخدمه يوميا قبل الاعتماد.

## 8. Create Saved Views for Role-Based Work

### English
1. Open the list page related to your role.
2. Apply your role filters.
3. Save the view with a role name:
   1. Warehouse - Today Receipts
   2. Sales - Pending Delivery
   3. Finance - Invoice Review
   4. Consignment - Draft Settlements
4. Set your main view as default if your role allows it.
5. Share naming standards with your team so everyone uses the same labels.

### العربية
1. افتح صفحة القائمة المناسبة لدورك.
2. طبق فلاتر الدور الوظيفي.
3. احفظ العرض باسم واضح للدور:
   1. Warehouse - Today Receipts
   2. Sales - Pending Delivery
   3. Finance - Invoice Review
   4. Consignment - Draft Settlements
4. اجعل العرض الرئيسي افتراضيا إذا كانت الصلاحيات تسمح بذلك.
5. شارك نمط التسمية مع فريقك حتى يستخدم الجميع نفس الأسماء.

## 9. Notification and Reminder Preferences

### English
1. Click profile icon, then open Notifications or My Settings.
2. Enable only useful alerts (document assignments, mentions, workflow actions).
3. Disable noisy alerts not relevant to your daily role.
4. Check Email Digest or reminder frequency.
5. Save settings.
6. Test by assigning one sample task to yourself and confirming alert delivery.

### العربية
1. اضغط أيقونة الحساب ثم افتح Notifications أو My Settings.
2. فعل التنبيهات المهمة فقط (التكليفات وmentions وإجراءات سير العمل).
3. أوقف التنبيهات المزعجة غير المرتبطة بعملك اليومي.
4. راجع إعدادات Email Digest أو تكرار التذكيرات.
5. احفظ الإعدادات.
6. اختبر ذلك بتعيين مهمة تجريبية لنفسك والتأكد من وصول التنبيه.

## 10. Daily Startup Checklist

### English
1. Log in and confirm correct language.
2. Confirm time zone/date/number format on one transaction.
3. Open your saved workspace shortcuts.
4. Apply your saved list filters.
5. Review new assignments and notifications.
6. Start with your priority queue (oldest pending first).

### العربية
1. سجل الدخول وتأكد من اللغة الصحيحة.
2. تأكد من إعدادات الوقت والتاريخ والأرقام على مستند واحد.
3. افتح الاختصارات المحفوظة في Workspace.
4. طبق الفلاتر المحفوظة.
5. راجع التكليفات الجديدة والتنبيهات.
6. ابدأ بقائمة الأولويات (الأقدم المعلق أولا).

## 11. Troubleshooting Quick Fixes

### English
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

### العربية
1. المشكلة: القوائم ما زالت بلغة غير صحيحة.
   الحل: افتح My Settings مرة أخرى، أعد اختيار اللغة، اضغط Save ثم حدث المتصفح بقوة.
2. المشكلة: الفلتر المحفوظ غير ظاهر.
   الحل: ارجع إلى القائمة، أعد تطبيق الفلتر، ثم احفظه باسم فريد.
3. المشكلة: التاريخ أو المبالغ تظهر بشكل خاطئ.
   الحل: راجع Date Format وNumber Format في My Settings.
4. المشكلة: اختصار اختفى من الصفحة.
   الحل: افتح Workspace وأعد تثبيت الاختصار.
5. المشكلة: لا توجد تنبيهات.
   الحل: راجع إعدادات التنبيهات وصلاحية إشعارات المتصفح.
6. المشكلة: تظهر صفحة 404 عند فتح localhost.
   الحل: تأكد أن frontend يعمل على المنفذ 8080 وافتح http://localhost:8080 في المتصفح.

## 12. Who to Contact (Escalation)

### English
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

### العربية
تواصل حسب الترتيب التالي:
1. قائد الفريق (أسئلة الدور أو الإجراء).
2. مالك العملية (سياسة العمل أو قواعد الاعتماد).
3. دعم ERP أو مكتب المساعدة (مشكلة نظام أو صلاحية أو خلل).

عند التصعيد، أرسل:
1. اسم المستخدم.
2. اسم الشاشة ونوع المستند.
3. الخطوات التي قمت بها.
4. لقطة شاشة للخطأ (إن وجدت).
5. وقت حدوث المشكلة.

## 13. One-Page Quick Checklist

### English - Quick Daily Card
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

### العربية - بطاقة تحقق يومية سريعة
1. تم تسجيل الدخول بنجاح.
2. تم اختيار اللغة الصحيحة.
3. تم التحقق من إعدادات الوقت والتاريخ والأرقام.
4. اختصارات Workspace جاهزة.
5. تم تحميل الفلاتر المحفوظة:
   1. PR - My Daily View
   2. DN - Daily Follow-up
   3. SI - Collection Focus
   4. CS - Daily Draft Check
6. تم تفعيل تنبيهات التكليفات وسير العمل.
7. تم بدء مهام الأولوية.
8. تم تصعيد المشاكل مع لقطة شاشة ووقت المشكلة.
