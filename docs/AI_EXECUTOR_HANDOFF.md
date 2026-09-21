# AI Executor Handoff Gate

الغرض من هذه الوثيقة تحديد متى يصبح المستودع ناضجًا بما يكفي لتسليمه إلى ذكاء اصطناعي منفذ دون أن يضطر لاختراع الـDomain أثناء البرمجة.

## الحالة

**NOT READY**

## لا يتم التسليم قبل تحقق البنود التالية

- [ ] Product Vision مستقرة ومقبولة.
- [ ] Domain Model يعرّف المفاهيم الرئيسية وعلاقاتها دون تناقضات كبيرة.
- [ ] Invariants معتمدة.
- [ ] الصلاحيات والـScope والـDelegation موضحة بما يكفي.
- [ ] Mission / Assignment / Team / Visit مفصولة دلاليًا.
- [ ] Draft / Submit / Finalize / Approve / Publish محددة المعنى.
- [ ] سيناريوهات Domain الأساسية مجتازة مفاهيميًا.
- [ ] Architecture decision للـModular Monolith والواجهات القابلة للاستبدال معتمدة.
- [ ] Minimal Stable Core محدد؛ لا توجد قائمة مفتوحة من Models بلا حدود.
- [ ] أول Vertical Slice محدد بمدخلاته ومخرجاته وAcceptance Criteria.
- [ ] ما هو داخل Scope أول إصدار وما هو Deferred موثق.
- [ ] استراتيجية الاختبار معروفة: unit/domain + integration + permissions + human acceptance.
- [ ] لا توجد قرارات Domain حرجة متروكة للمنفذ كي يخمنها.

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

## مسؤولية المراجعة

بلوغ READY قرار تصميم، وليس مجرد اكتمال ملفات. يجب مراجعته صراحة قبل بدء التنفيذ.
