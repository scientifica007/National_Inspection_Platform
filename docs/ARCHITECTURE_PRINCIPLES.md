# Architecture Principles

## القرار العام

نبدأ بـ **Modular Monolith** بحدود Domain واضحة. لا نبدأ بـ microservices.

الهدف هو "قطع غيار" قابلة للاستبدال، لكن بحدود وعقود واضحة بدل تفكيك مبكر يزيد الصيانة تعقيدًا.

## الطبقات

```text
Presentation
    ↓
Application
    ↓
Domain
    ↓
Ports
    ↓
Infrastructure Adapters
```

### Domain
قواعد العمل والمفاهيم الأساسية.  
لا يعتمد على HTML أو CSS أو قاعدة بيانات بعينها أو framework واجهة معين.

### Application
Use cases وتنسيق العمليات: إنشاء مهمة، قبول مهمة، تثبيت زيارة، اعتماد مرجع، إلخ.

### Presentation
واجهة الويب الحالية. يجب أن تكون قابلة لإعادة التصميم دون إعادة كتابة الـDomain.

### Infrastructure
قاعدة البيانات، الملفات، البريد، التصدير، البحث، التكاملات الخارجية. تدخل خلف Interfaces/Ports.

## Frontend قابل للتغيير

للسماح بإعادة تصميم الواجهة مرارًا حتى الوصول إلى الشكل المقبول:

- لا Business Logic داخل templates أو JavaScript الخاص بالشكل.
- Design Tokens للألوان والمسافات والخطوط والحالات.
- Component Library صغيرة وموحدة.
- Layouts منفصلة عن Domain/use-case logic.
- View Models/Presenters تحول بيانات التطبيق إلى ما تحتاجه الشاشة.
- RTL وAccessibility من البداية.
- لا تربط الاختبارات الوظيفية الجوهرية بأسماء CSS أو تفاصيل شكلية.
- يمكن لاحقًا استبدال server-rendered UI بواجهة أخرى أو إضافة API دون تغيير الـDomain.

## Backend قابل للصيانة

كل مجال وظيفي يكون Module بواجهة عامة صغيرة، مثل:

- identity
- organization
- geography
- institutions
- knowledge
- missions
- visits
- records
- reporting

القواعد:

- لا يصل Module إلى جداول Module آخر مباشرة إلا عبر عقود مصممة.
- لا circular dependencies.
- العمليات العابرة للوحدات تنسقها Application Services.
- Domain Events تستخدم عندما يوجد سبب حقيقي، لا لمجرد "حداثة" التصميم.
- كل Module يملك اختبارات قواعده الأساسية.
- migrations صغيرة وقابلة للمراجعة.
- لا Generic Entity-Attribute-Value كحل شامل؛ المرونة لا تعني فقدان المعنى.

## قاعدة الاستبدال

نعتبر الجزء "قابلًا للاستبدال" إذا أمكن تغييره مع بقاء:

1. Domain invariants كما هي.
2. Public contract للوحدة واضحًا.
3. اختبارات العقد تمر.
4. البيانات التاريخية لا تفقد معناها.
5. الأجزاء الأخرى لا تحتاج تعديلًا واسعًا.

## أمثلة

- تغيير الثيم أو Layout: يجب ألا يمس Domain/Application.
- استبدال صفحة Dashboard بالكامل: يجب أن تعتمد نفس Query contracts.
- تغيير محرك التصدير PDF: خلف Export Port.
- الانتقال من تخزين ملفات محلي إلى Object Storage: خلف Storage Port.
- إضافة REST API أو واجهة هاتف: Presentation Adapter جديد.
- تغيير PostgreSQL مستقبلًا: ممكن نظريًا خلف persistence abstractions، لكن لا نبالغ في إخفاء قدرات قاعدة البيانات إذا كان ذلك يضر البساطة.

## فلسفة الصيانة

الأولوية ليست لأقصى abstraction، بل لأوضح boundaries وأقل coupling ممكن مع أقل تعقيد مفيد.
