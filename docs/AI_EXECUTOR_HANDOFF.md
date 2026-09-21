# AI Executor Handoff Gate

الغرض من هذه الوثيقة تحديد متى يصبح المستودع ناضجًا بما يكفي لتسليمه إلى ذكاء اصطناعي منفذ دون أن يضطر لاختراع الـDomain أثناء البرمجة.

## الحالة

**READY FOR AI EXECUTOR — CONTROLLED IMPLEMENTATION**

Readiness applies to:

**Vertical Slice 01 — Solo Inspector Field Visit**

It does not authorize implementation of the full national platform.

## Gate checklist

- [x] Product Vision مستقرة ومقبولة baseline.
- [x] Domain Model يعرّف المفاهيم الرئيسية وعلاقاتها دون تناقضات مانعة لأول Slice.
- [x] Invariants معتمدة baseline.
- [x] الصلاحيات والـScope والـDelegation موضحة بالقدر اللازم لأول تنفيذ.
- [x] Admin authority منفصلة صراحة عن professional authorship.
- [x] Mission / Assignment / Team / Visit مفصولة دلاليًا في التصميم.
- [x] Draft / Submit / Finalize / Approve / Publish محددة المعنى العام.
- [x] سيناريوهات Domain الأساسية راجعت مفاهيميًا.
- [x] Architecture decision للـModular Monolith والواجهات القابلة للاستبدال معتمدة.
- [x] Minimal Stable Core محدد.
- [x] أول Vertical Slice محدد بمدخلاته ومخرجاته وAcceptance Criteria.
- [x] ما هو داخل Scope أول تنفيذ وما هو Deferred موثق.
- [x] استراتيجية الاختبار معروفة.
- [x] Module dependency map والتنظيم الهندسي لأول تنفيذ محددان.
- [x] Concrete data model لأول Vertical Slice محدد ومراجع.
- [x] Stack أول تنفيذ موثق ومعتمد.
- [x] Engineering conventions موثقة.
- [x] Owner-level blocking decisions resolved.
- [x] مراجعة نهائية للتناقضات وOver-abstraction مكتملة.
- [x] Executor Specification جاهزة.
- [x] Executor Prompt جاهز.

## Authorized implementation boundary

The executor may build only what is defined in:

- `docs/AI_EXECUTOR_SPEC_01.md`
- `docs/VERTICAL_SLICE_01.md`
- `docs/VERTICAL_SLICE_01_DATA_MODEL.md`
- `docs/INITIAL_IMPLEMENTATION_SCOPE.md`

Anything explicitly deferred remains deferred.

## Mandatory executor rules

- عدم توسيع النطاق من نفسه.
- عدم كسر Invariants.
- احترام حدود Modules.
- بناء واختبار Vertical Slice كامل.
- توثيق أي قرار جديد بدل إخفائه في الكود.
- التوقف عند تعارض Domain حقيقي بدل اختراع سياسة تنظيمية.
- عدم استعارة كود أو Architecture من المشاريع التجريبية السابقة.
- عدم تحويل Admin إلى وسيلة impersonation.
- عدم جعل الواجهة مصدرًا وحيدًا لتطبيق الصلاحيات أو immutability.
- عدم إضافة future modules كقوالب فارغة لمجرد أنها مذكورة في الرؤية.

## Handoff package

Primary:
- `docs/AI_EXECUTOR_PROMPT_01.md`
- `docs/AI_EXECUTOR_SPEC_01.md`

Supporting:
- `docs/PRODUCT_VISION.md`
- `docs/INVARIANTS.md`
- `docs/AUTHORITY_MODEL.md`
- `docs/LIFECYCLE_SEMANTICS.md`
- `docs/LIFECYCLE_PROFILES.md`
- `docs/MINIMAL_STABLE_CORE.md`
- `docs/MODULE_DEPENDENCY_MAP.md`
- `docs/ENGINEERING_CONVENTIONS.md`
- accepted ADRs.

## Important limitation

**READY** means "ready to implement Slice 01 safely", not "all future domain design is finished".

Future slices still require their own design/readiness gates.
