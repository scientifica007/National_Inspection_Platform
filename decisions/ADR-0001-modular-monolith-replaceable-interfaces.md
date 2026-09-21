# ADR-0001 — Modular Monolith with Replaceable Interfaces

- Status: **Accepted for M0**
- Date: 2026-09-21

## Context

المنصة متوقعة أن تتطور وظيفيًا وبصريًا على مدى طويل. المطلوب حرية كبيرة في تغيير الواجهة، وإضافة أو تعديل مجالات عمل، مع صيانة بسيطة نسبيًا وتجنب هدم النظام عند كل تغيير.

## Decision

نستخدم **Modular Monolith** في البداية، مع فصل واضح بين Domain وApplication وPresentation وInfrastructure.

نعتبر الواجهة Presentation Adapter وليست مكانًا لقواعد العمل.  
نضع التكاملات التقنية خلف Ports/Interfaces عندما توجد فائدة عملية لذلك.  
نستخدم Design System وComponent Library وDesign Tokens لتسهيل إعادة تصميم الواجهة.

## Why not Microservices now?

- تضيف عبئًا تشغيليًا وتوزيعيًا لا نحتاجه في البداية.
- تجعل المعاملات والتشخيص والاختبارات والصيانة أصعب.
- لا توجد بعد حدود حمل أو استقلال نشر تبررها.

يمكن استخراج Module إلى Service مستقل مستقبلًا إذا ظهرت حاجة حقيقية وكان العقد بين الوحدات ناضجًا.

## Consequences

### Positive
- إعادة تصميم الواجهة لا تمس منطق العمل.
- يمكن صيانة الوحدات واختبارها بمعزل نسبي.
- التطوير الأولي أبسط من الأنظمة الموزعة.
- توجد طريق واضحة للتوسع دون التزام مبكر ببنية معقدة.

### Costs
- يتطلب انضباطًا حقيقيًا في حدود Modules.
- Modular Monolith يمكن أن يتحول إلى Big Ball of Mud إذا سُمِح بوصول عشوائي بين الوحدات.
- بعض الاستبدالات ستظل تحتاج migrations أو adapters؛ "قابل للاستبدال" لا يعني "صفر تكلفة".

## Guardrail

أي تغيير جديد يجب أن يجيب: هل هذا Domain rule، Application use case، Presentation concern، أم Infrastructure concern؟  
إذا اختلطت أكثر من طبقة في نفس المكان بلا سبب واضح، يجب مراجعة التصميم قبل الدمج.
