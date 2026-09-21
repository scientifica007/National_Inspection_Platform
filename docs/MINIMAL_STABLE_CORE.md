# Minimal Stable Core

## الهدف

تحديد أصغر نواة مفاهيمية تكفي لبدء البناء من دون تحويل المنصة إلى مخطط ضخم أو إغلاق الطريق أمام التطور.

هذه الوثيقة تميز بين:

- **Core concepts**: مفاهيم يجب أن تكون مستقرة نسبيًا.
- **Relations / child entities**: لا تحتاج Aggregate Root مستقلًا بالضرورة.
- **Deferred concepts**: مهمة، لكن لا تدخل أول تنفيذ قبل الحاجة.

## النواة المستقرة المقترحة

### 1. Person
يمثل الإنسان نفسه، مستقلًا عن الحساب والرتبة والدور المؤقت.

يملك تاريخ علاقات مهنية وتنظيمية، لكنه لا يخزن "الحقيقة الحالية" كحقول جامدة عندما تكون زمنية.

### 2. Account
هوية الدخول والأمان المرتبطة بشخص.  
لا تمثل الرتبة المهنية ولا الدور التشغيلي.

### 3. OrganizationUnit
وحدة تنظيمية قابلة للتكوين، مثل وزارة أو مديرية أو مصلحة أو مقاطعة.  
لا نفترض شجرة قانونية واحدة ثابتة لكل الأزمنة.

### 4. GeographicUnit
كيان جغرافي مثل ولاية أو دائرة أو بلدية مع صلاحية زمنية وعلاقات جغرافية مؤرخة.

### 5. Institution
المؤسسة محل العمل/المتابعة/التفتيش.  
تنشأ محليًا أو تشترك أو تعتمد وفق الصلاحيات، ولا تكون قائمة ثابتة في الكود.

### 6. Team
مجموعة عمل مستقلة عن أعضائها الحاليين.  
العضوية والقيادة والمسؤوليات علاقات زمنية وسياقية.

### 7. KnowledgeArtifact
جذر مشترك للمحتوى المعرفي القابل للإصدار والمشاركة، مع أنواع دلالية واضحة مثل:
- Reference
- Checklist
- Criterion set
- Indicator set
- Legal reference collection
- Guide

الهدف من الجذر المشترك توحيد الملكية والإصدار والنطاق والتاريخ، لا إذابة الفروق الدلالية بين الأنواع.

### 8. Mission
يمثل عملًا مطلوبًا أو مقترحًا أو مفتوحًا.  
قد يكون اختياريًا أو إلزاميًا أو مختلطًا، فرديًا أو جماعيًا، عالي الحرية أو شديد التحديد.

### 9. Activity
يمثل عملًا منفذًا فعليًا.  
قد يكون مرتبطًا بمهمة أو مستقلاً عنها.

**Visit** تخصص دلالي من Activity للعمل الميداني، ولا نجعل كل نشاط Visit.

### 10. Record
جذر للسجل المهني المثبت: معاينة، توصية، قرار، ملاحظة مهنية، أو نتيجة موثقة.  
قبل التثبيت يكون Draft قابلًا للتغيير؛ بعد التثبيت يصبح غير قابل لإعادة الكتابة.

### 11. Report
مخرج مركب يربط سجلات ومصادر ومساهمات وجداول، مع حفظ provenance.

## علاقات لا تحتاج جذورًا مستقلة مبدئيًا

- PositionAssignment
- CapabilityGrant
- Delegation
- TeamMembership
- TeamResponsibility
- OrganizationalRelationship
- GeographicRelation
- PersonGeographicRelation
- MissionParticipation
- Assignment
- EligibilityRule
- KnowledgeArtifactVersion
- EvidenceAttachment
- Amendment

يمكن ترقية أي منها إلى Aggregate Root لاحقًا إذا ظهرت حاجة حقيقية للاستقلال في lifecycle أو concurrency أو ownership.

## ما يؤجل عن أول Vertical Slice

- فرق معقدة ومتعددة المستويات.
- Delegation المتقدم.
- المهام الجماعية متعددة الفرق.
- recurring teams / recurring missions.
- Dataset engine عام.
- dashboards وطنية متقدمة.
- integrations خارجية.
- workflow builder عام.
- notification engine عام.
- microservices.
- generic rule engine.
- generic EAV modeling.

## اختبار البساطة

لا يضاف Aggregate Root جديد إلا إذا فشل أحد الشروط التالية:

1. المفهوم لا يمكن تمثيله كعلاقة أو child entity بوضوح.
2. له lifecycle مستقل حقيقي.
3. يحتاج صلاحيات/ملكية مستقلة.
4. يحتاج معاملات أو versioning مستقلاً.
5. غيابه سيؤدي إلى coupling أو special cases أسوأ من إضافته.

## قاعدة التصميم

**Prefer explicit domain meaning over generic abstraction.**

المرونة تأتي من العلاقات والتهيئة والنطاق والزمن، لا من تحويل كل شيء إلى Entity/Property/Relation عامة بلا معنى مهني.
