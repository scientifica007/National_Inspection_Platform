# Domain Model v2 — Accepted Conceptual Baseline

- Status: **Accepted baseline for Vertical Slice 01**
- Owner approval: 2026-09-21

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

## النواة المفاهيمية

### Identity & Authority
- Person
- Account
- PositionAssignment
- CapabilityGrant
- Delegation

### Organization & Teams
- OrganizationUnit
- Team
- TeamCycle
- TeamMembership
- TeamResponsibility
- OrganizationalRelationship

**Team** يحتفظ بهويته عبر الزمن.  
**TeamCycle** يمثل دورة/فترة تشغيلية موسمية أو دورية، مثل فريق دخول تكويني في سبتمبر–أكتوبر، دون إنشاء معنى جديد للفريق كل مرة.

### Geography
- GeographicUnit
- GeographicRelation
- PersonGeographicRelation

العلاقات الجغرافية مؤرخة، حتى يبقى التاريخ قابلًا للتفسير عند تغير التقسيم الإداري.

### Institutions
- Institution
- InstitutionRelationship
- InstitutionLifecycle

المؤسسات Data وليست قائمة ثابتة في الكود.

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

Mission تمثل العمل المطلوب/المقترح/المفتوح.  
Activity تمثل التنفيذ الفعلي.  
Visit نوع مهني ميداني من Activity.  
يمكن أن توجد Activity/Visit مستقلة بلا Mission.

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

## Scope

Scope ليست hierarchy صلبة واحدة.

الأشكال المفاهيمية:
- OWN
- NATIONAL
- ORGANIZATION(id)
- GEOGRAPHY(id)
- TEAM(id)
- INSTITUTION(id)
- MISSION(id)

تقاطع القيود هو القاعدة عند اجتماعها داخل نفس السلطة. الاتحاد يحتاج Grants/Policy صريحة.

## علاقات أساسية

- الشخص قد يشغل أكثر من Position عبر الزمن.
- الشخص قد ينتمي إلى عدة فرق في الوقت نفسه.
- القيادة علاقة سياقية وزمنية، وليست هرمية قانونية ثابتة.
- الفريق مستقل عن أعضائه الحاليين.
- الفريق الدوري يحتفظ بهويته عبر TeamCycle.
- Mission قد تكون اختيارية أو إلزامية أو مختلطة.
- المحتوى المتغير يمثل كبيانات/تهيئة كلما أمكن.
- الزيارات والتنفيذ تعتمد Snapshot يحفظ المعنى التاريخي.
- local source referenced by finalized history لا يحذف بطريقة تكسر التاريخ؛ يمكن archive/tombstone مع بقاء snapshot.
- Admin authority منفصلة عن professional authorship.
