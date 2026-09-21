# AI Executor Handoff Gate

الغرض من هذه الوثيقة تحديد متى يصبح المستودع ناضجًا بما يكفي لتسليمه إلى ذكاء اصطناعي منفذ دون أن يضطر لاختراع الـDomain أثناء البرمجة.

## الحالة

**NOT READY**

## لا يتم التسليم قبل تحقق البنود التالية

- [ ] Product Vision مستقرة ومقبولة نهائيًا.
- [ ] Domain Model يعرّف المفاهيم الرئيسية وعلاقاتها دون تناقضات كبيرة بعد مراجعة السيناريوهات.
- [ ] Invariants معتمدة نهائيًا.
- [ ] الصلاحيات والـScope والـDelegation موضحة ومختبرة مفاهيميًا بما يكفي.
- [x] Mission / Assignment / Team / Visit مفصولة دلاليًا في التصميم.
- [x] Draft / Submit / Finalize / Approve / Publish محددة المعنى العام.
- [ ] سيناريوهات Domain الأساسية مجتازة مفاهيميًا، لا مجرد مكتوبة.
- [x] Architecture decision للـModular Monolith والواجهات القابلة للاستبدال معتمدة.
- [x] Minimal Stable Core محدد؛ لا توجد قائمة مفتوحة من Models بلا حدود.
- [x] أول Vertical Slice محدد بمدخلاته ومخرجاته وAcceptance Criteria.
- [x] ما هو داخل Scope أول تنفيذ وما هو Deferred موثق.
- [x] استراتيجية الاختبار معروفة: domain + application + integration + permissions + human acceptance.
- [ ] Module dependency map والتنظيم الهندسي لأول تنفيذ محددان.
- [ ] Concrete data model لأول Vertical Slice محدد ومراجع.
- [ ] Stack أول تنفيذ موثق ومبرر.
- [ ] لا توجد قرارات Domain حرجة متروكة للمنفذ كي يخمنها.
- [ ] مراجعة نهائية للتناقضات وOver-abstraction مكتملة.

## معنى READY

عند تحقق البنود أعلاه تتحول الحالة إلى:

**READY FOR AI EXECUTOR — CONTROLLED IMPLEMENTATION**

ويجب أن يحصل المنفذ على Prompt تنفيذي يفرض:

- عدم توسيع النطاق من نفسه.
- عدم كسر Invariants.
- احترام حدود Modules.
- بناء واختبار Vertical Slice كامل.
- توثيق أي قرار جديد بدل إخفائه في الكود.
- التوقف عند تعارض Domain حقيقي بدل اختراع سياسة تنظيمية.
- عدم استعارة كود أو Architecture من المشاريع التجريبية السابقة إلا إذا صدر قرار صريح بذلك.

## مسؤولية المراجعة

بلوغ READY قرار تصميم، وليس مجرد اكتمال ملفات. يجب مراجعته صراحة قبل بدء التنفيذ.

## آخر checkpoint

تم تحديد:
- Minimal Stable Core.
- Authority Model draft.
- Lifecycle semantics.
- Vertical Slice 01.
- Initial implementation scope.
- Test strategy.

تبقى مراجعة السيناريوهات، نموذج البيانات التفصيلي للـSlice الأول، dependency map، واختيار الـstack قبل handoff.
