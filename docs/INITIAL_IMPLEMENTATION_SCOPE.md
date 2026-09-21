# Initial Implementation Scope

## الهدف

منع أول منفذ من تفسير الرؤية الكاملة على أنها أمر لبناء المنصة الوطنية كلها دفعة واحدة.

## In Scope — أول تنفيذ

يطابق **Vertical Slice 01** فقط:

- authentication لحساب Admin وInspector تجريبيين.
- Person/Account minimal mapping.
- capability checks اللازمة للمسار.
- Institution محلية بسيطة.
- KnowledgeArtifact/Checklist محلية بسيطة.
- Visit فردية مستقلة.
- frozen checklist snapshot.
- finding + recommendation.
- Draft / Finalize.
- immutable finalized records.
- minimal audit/provenance.
- Admin read-only oversight على السجل المهني المثبت.
- RTL responsive UI.
- design tokens + reusable components بالحد الأدنى.

## Explicitly Deferred

- Minister dashboard.
- Inspector General dashboard.
- Central Inspector team leadership.
- Team engine.
- Mission engine.
- optional/mandatory assignment.
- Delegation.
- organizational hierarchy builder.
- geographic history management UI.
- publishing/approval workflows.
- report aggregation.
- spreadsheets/datasets.
- advanced analytics.
- notifications.
- APIs for third-party systems.
- mobile native app.
- microservices.
- AI features.

## Rule

Deferred does not mean rejected.  
It means: **the architecture must not block it, but the first implementation must not build it.**

## Compatibility requirement

أي قرار في Slice 01 يجب ألا يجعل إضافة Team/Mission/Assignment لاحقًا تتطلب إعادة تعريف معنى Person, Visit, Record أو Finalization.
