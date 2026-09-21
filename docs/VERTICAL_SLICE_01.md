# Vertical Slice 01 — Solo Inspector Field Visit

## لماذا هذا الـSlice؟

نحتاج أول تنفيذ صغير لكنه يختبر أهم مبادئ المنصة فعليًا:

- هوية وصلاحيات.
- حرية المفتش في العمل الفردي.
- مؤسسة قابلة للإنشاء كبيانات.
- مرجع/Checklist محلي قابل للاستعمال.
- زيارة ميدانية.
- معاينات وتوصيات.
- تثبيت غير قابل لإعادة الكتابة.
- رؤية Admin من دون امتلاك أو إعادة كتابة عمل المفتش.
- واجهة قابلة لإعادة التصميم من دون خلط Business Logic بها.

لا ندخل Teams أو المهام الجماعية أو Dashboards الوطنية في هذا الـSlice.

## Actors

### Inspector
يستطيع ضمن نطاقه:
- إنشاء مؤسسة محلية.
- إنشاء Checklist بسيطة محلية.
- إنشاء زيارة مستقلة.
- اختيار مؤسسة وChecklist.
- تسجيل findings/recommendations.
- حفظ Draft.
- Finalize للزيارة/السجلات وفق القواعد.

### Admin
- يرى الزيارة.
- يرى مصدرها وصاحبها.
- لا يعدل finding/recommendation مثبتة نيابة عن المفتش.
- يستطيع إدارة الحسابات والصلاحيات اللازمة للـSlice.

## Happy Path

```text
Inspector logs in
  ↓
creates local institution
  ↓
creates local checklist
  ↓
creates draft visit
  ↓
selects institution + checklist snapshot
  ↓
records findings/recommendations
  ↓
saves and edits draft
  ↓
finalizes
  ↓
record becomes immutable
  ↓
Admin can inspect the result and provenance
```

## Required Domain Behavior

1. المؤسسة ليست hard-coded.
2. الـChecklist ليست hard-coded.
3. Snapshot الزيارة لا يتغير إذا عدلت الـChecklist الأصلية لاحقًا.
4. Draft يمكن تعديله وحذفه.
5. Finalized record لا يمكن تعديله أو حذفه.
6. actor/author محفوظان.
7. Admin visibility لا تعطيه حق إعادة كتابة السجل.
8. محاولة تغيير سجل مثبت ترفض من Application/Domain layer، لا من إخفاء زر فقط.

## UI Minimum

- Login.
- Inspector dashboard بسيط.
- My institutions.
- My knowledge/checklists.
- My visits.
- Visit editor.
- Finalization confirmation.
- Read-only finalized view.
- Admin view.

هذه واجهة إثبات وليست التصميم النهائي.

## Acceptance Criteria

- [ ] يمكن للمفتش إكمال Happy Path من المتصفح دون Admin.
- [ ] يمكن إنشاء Institution محلية دون تعديل code/config file.
- [ ] يمكن إنشاء Checklist محلية من الواجهة.
- [ ] Visit تحفظ نسخة frozen من checklist المستخدمة.
- [ ] تعديل checklist بعد إنشاء snapshot لا يغير الزيارة.
- [ ] Draft visit editable.
- [ ] Draft visit deletable.
- [ ] Finalized visit/records reject update server-side.
- [ ] Finalized visit/records reject delete server-side.
- [ ] Admin يستطيع القراءة.
- [ ] Admin لا يستطيع انتحال inspector لتعديل سجله.
- [ ] audit/provenance يبين actor + timestamps الأساسية.
- [ ] تغيير theme/layout لا يغير اختبارات Domain/Application.
- [ ] mobile RTL usable في المسار الكامل.

## Out of Scope

- Mission assignment.
- Teams.
- approval/publishing of local content.
- geographic historical versioning UI.
- national dashboard.
- report composer.
- datasets.
- notifications.
- external integrations.

## Gate

لا ينتقل التنفيذ إلى Slice 02 قبل:
- automated tests passing.
- permission tests passing.
- human acceptance على desktop وmobile.
- توثيق أي UX/domain gap ظهر أثناء التجربة.
