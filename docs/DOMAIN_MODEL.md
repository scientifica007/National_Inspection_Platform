# Domain Model v2 — Conceptual Draft

## قاعدة الفصل

نفصل بين:

- **Person**: الإنسان.
- **Account**: وسيلة الدخول.
- **Position**: الصفة الرسمية أو المهنية.
- **Operational Role**: الدور المؤقت في فريق أو مهمة.
- **Capability**: ما يسمح للشخص بفعله.
- **Scope**: أين وعلى ماذا تسري الصلاحية.
- **Time**: متى تسري العلاقة أو الصلاحية.
- **Context**: الفريق أو المهمة أو الوحدة التنظيمية التي تعطي العلاقة معناها.

## النواة المقترحة

### Identity & Authority
- Person
- Account
- PositionAssignment
- CapabilityGrant
- Delegation

### Organization & Teams
- OrganizationUnit
- Team
- TeamMembership
- TeamResponsibility
- OrganizationalRelationship

### Geography
- GeographicUnit
- GeographicRelation
- PersonGeographicRelation

### Institutions
- Institution
- InstitutionRelationship
- InstitutionLifecycle

### Knowledge
- Reference
- Checklist
- Criterion
- Indicator
- LegalReference
- Guide
- KnowledgeArtifactVersion

### Work
- Mission
- EligibilityRule
- MissionParticipation
- Assignment
- Activity
- Visit

### Evidence & Records
- Finding
- Recommendation
- Decision
- Evidence
- FinalizedRecord
- Amendment

### Reporting & Data
- Report
- Dataset
- MetricSnapshot
- Aggregation/View

## علاقات أساسية

- الشخص قد يشغل أكثر من Position عبر الزمن.
- الشخص قد ينتمي إلى عدة فرق في الوقت نفسه.
- القيادة علاقة سياقية وزمنية، وليست هرمية قانونية ثابتة.
- الفريق كيان مستقل عن أعضائه؛ تغيير الأعضاء لا يمحو هوية الفريق.
- الوحدة الجغرافية والعلاقات الجغرافية قابلة للتأريخ.
- Mission تمثل العمل المطلوب أو المقترح؛ Visit تمثل حدث تنفيذ ميداني فعلي.
- Mission قد تكون اختيارية أو إلزامية أو مختلطة.
- Activity قد توجد دون Mission عندما يعمل المفتش ضمن استقلاليته المهنية.
- المحتوى المعرفي والإداري المتغير يمثل كبيانات، لا كقوائم ثابتة في الكود كلما أمكن.
- الزيارات والتنفيذ يعتمدون نسخًا Snapshot من المراجع المستخدمة حتى لا تتغير دلالة التاريخ بأثر رجعي.
