# National Inspection Platform

منصة وطنية مرنة لإدارة أعمال التفتيش، صُممت كبداية نظيفة مستقلة عن المشاريع التجريبية السابقة.

## الحالة الحالية

**M0 — Foundation / Domain Design**

لا يوجد كود تطبيق بعد. الهدف الحالي هو تثبيت النموذج المفاهيمي والقواعد المعمارية قبل اختيار التفاصيل التنفيذية.

## المبادئ المؤسسة

1. **Stable Core** — نواة مفاهيمية صغيرة وثابتة نسبيًا.
2. **Flexible Reality** — الواقع التنظيمي والجغرافي والمهني يُمثَّل كبيانات وتهيئة كلما أمكن، لا كافتراضات صلبة داخل الكود.
3. **Immutable History** — السجلات المثبتة لا يُعاد كتابتها؛ التصحيح يتم بإضافة سجل تاريخي جديد.
4. **Progressive Complexity** — لا نضيف تعقيدًا إلا عندما تبرره حاجة حقيقية.
5. **Replaceable Parts** — واجهات النظام ووحداته التنفيذية تُبنى بحدود واضحة تسمح بالتغيير والصيانة دون هدم المنصة.
6. **Freedom by Default, Constraint by Rule** — الحرية هي الأصل، والقيد لا يفرض إلا لقاعدة مبررة وصريحة.

## منهج البناء

المنصة ستبدأ كـ **Modular Monolith** بحدود Domain واضحة، لا كـ microservices.  
الـDomain والـApplication Logic لا يعتمدان على شكل الواجهة. واجهة المستخدم طبقة قابلة للتغيير، والـInfrastructure قابل للاستبدال خلف عقود واضحة.

## المسار المبدئي

- M0: Foundation / Domain
- M1: Identity + People + Authority
- M2: Geography + Organizations + Institutions
- M3: Knowledge / References
- M4: Missions + Teams + Assignments
- M5: Activities + Visits
- M6: Findings + Recommendations + Evidence
- M7: Finalization + Immutable History
- M8: Reports + Datasets
- M9: Dashboards + Semantic Zoom
- M10: Human Pilot

لن يبدأ التنفيذ البرمجي قبل اجتياز **AI Executor Handoff Gate** الموثق في `docs/AI_EXECUTOR_HANDOFF.md`.

## وثائق M0

- `docs/PRODUCT_VISION.md`
- `docs/DOMAIN_MODEL.md`
- `docs/INVARIANTS.md`
- `docs/ARCHITECTURE_PRINCIPLES.md`
- `docs/SCENARIO_TESTS.md`
- `docs/AI_EXECUTOR_HANDOFF.md`
- `decisions/ADR-0001-modular-monolith-replaceable-interfaces.md`
