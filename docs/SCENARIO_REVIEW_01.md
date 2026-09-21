# Scenario Review 01 — Conceptual Fitness

## الهدف

مراجعة السيناريوهات الواقعية مقابل Minimal Stable Core، واكتشاف الأماكن التي ما زالت تحتاج قرارًا قبل التنفيذ.

## النتيجة العامة

النموذج الحالي يمثل معظم السيناريوهات دون hard-coded hierarchy أو special-case code. ظهرت أربع نقاط تحتاج ضبطًا إضافيًا، لكنها لا تتطلب تغيير الاتجاه المعماري.

## Matrix

| # | Scenario | Representation | Status |
|---|---|---|---|
| 1 | مفتش يعمل منفردًا | Person + Activity/Visit بلا Mission | PASS |
| 2 | عضو في فريقين | TeamMembership متعدد بزمن/دور | PASS |
| 3 | مركزي تحت قيادة مركزي آخر مؤقتًا | Position ثابت + TeamResponsibility سياقية | PASS |
| 4 | فريق جغرافي تتغير عضويته | Team identity + memberships temporal | PASS |
| 5 | فريق موسمي يتكرر | Team + **TeamCycle** child entity | REFINEMENT |
| 6 | المفتش العام يقود فريقًا مباشرة | TeamResponsibility | PASS |
| 7 | مهمة اختيارية لفئة مؤهلة | Mission + EligibilityRule + Participation | PASS |
| 8 | تتحول المهمة لتكليف | Mission + Assignment | PASS |
| 9 | مهمة تحدد المخرجات فقط | required_outputs مع method غير مقيد | PASS |
| 10 | مهمة تحدد خطوات إلزامية | Mission constraints | PASS |
| 11 | مؤسسة محلية ثم اقتراح اعتماد | Institution lifecycle + ownership/scope | PASS |
| 12 | Checklist محلية ثم تعميم | KnowledgeArtifact versions + publish scope | PASS |
| 13 | Visit تستخدم v3 ثم يظهر v4 | frozen snapshot | PASS |
| 14 | Finding مثبت ثم تصحيح | Finalized Record + Amendment | PASS |
| 15 | تقرير فريق من مساهمات متعددة | Report + source records + provenance | PASS |
| 16 | تغير علاقة البلدية إداريًا | GeographicRelation valid_from/to | PASS |
| 17 | سكن/تكفل/عمل في ولايات مختلفة | PersonGeographicRelation typed | PASS |
| 18 | Dashboard وطني مع drill-down | read/query models over shared facts | PASS |
| 19 | Dashboard المفتش الشخصي | scoped read/query models | PASS |
| 20 | تغيير الواجهة بالكامل | Presentation replacement contract | PASS |

## Refinement 1 — TeamCycle

الفريق المتكرر لا يعاد اختزاله إلى status يتغير ذهابًا وإيابًا بلا تاريخ.

نضيف child entity مفاهيمي:

```text
Team
  └── TeamCycle
        ├── valid_from
        ├── valid_until
        ├── purpose/context
        └── status
```

العضوية والمسؤوليات يمكن ربطها بالـTeam وبـTeamCycle عند الحاجة.

هذا يسمح بفريق جغرافي ثابت الهوية ودورات سبتمبر/أكتوبر أو يناير/مارس مستقلة تاريخيًا.

## Refinement 2 — Scope composition

Scope ليس string واحدة. نحتاج semantics واضحة لتركيب النطاقات.

مبدئيًا:

```text
Scope =
  OWN
  | NATIONAL
  | ORGANIZATION(id)
  | GEOGRAPHY(id)
  | TEAM(id)
  | INSTITUTION(id)
  | MISSION(id)
```

وعند وجود أكثر من قيد فإن الصلاحية الفعلية هي **تقاطع القيود** لا جمعها افتراضيًا.

مثال:
- capability = VIEW_VISIT
- geography = Tébessa
- team = Team A

النتيجة: زيارات Team A الواقعة ضمن Tébessa، لا كل تبسة + كل Team A.

الـunion يحتاج Grant منفصلًا أو Policy صريحة.

## Refinement 3 — Local deletion vs historical use

"Local" لا يعني أن حذف المصدر يستطيع كسر سجل مثبت.

القاعدة المقترحة:

- local draft/unreferenced: hard delete allowed.
- local active but only in drafts: delete/cascade drafts حسب policy.
- referenced by finalized record: source may be archived/tombstoned, بينما snapshot التاريخي يبقى دائمًا.

## Refinement 4 — Administrative authority vs professional authorship

Admin يستطيع إدارة النظام ورؤية البيانات وإدارة الصلاحيات، لكن توجد مسألة Domain تحتاج قرارًا صريحًا:

**هل Admin بصفته Admin فقط يستطيع إنشاء وتثبيت معاينة مهنية باسمه، أم يحتاج أيضًا إلى Position/Professional Capability مناسبة؟**

الاتجاه المقترح حاليًا:
- Admin administrative power لا تساوي professional authorship.
- إذا كان الشخص نفسه Inspector/Minister/etc فيحصل على الصلاحية المهنية بصفته المهنية ويسجل الفعل بهويته الحقيقية.
- Admin لا ينتحل Inspector.

هذه النقطة تبقى OPEN حتى اعتمادها صراحة.

## Conclusion

لا توجد حتى الآن حاجة إلى:
- hierarchy صلبة.
- microservices.
- generic EAV.
- generic workflow engine.

النموذج صالح للاستمرار، مع TeamCycle وScope semantics وقاعدة retention المحلية، وبقاء سؤال Admin/professional authorship مفتوحًا.
