# Test Strategy

## 1. Domain Tests

اختبارات سريعة بلا UI لقواعد مثل:

- Draft mutable.
- Finalized immutable.
- Amendment adds history.
- snapshot meaning frozen.
- authority respects scope.
- identity cannot be borrowed.

## 2. Application / Use-case Tests

تختبر المسارات:

- create institution.
- create checklist.
- create visit.
- finalize visit.
- permission denials.
- admin read-only oversight.

## 3. Integration Tests

- ORM/database constraints.
- transactions.
- snapshot persistence.
- authentication integration.
- audit/provenance writes.

## 4. Permission Matrix Tests

كل endpoint/use case حساس يجب اختباره على الأقل لـ:

- unauthenticated.
- owner inspector.
- different inspector.
- admin.

لا يكفي إخفاء الزر في UI.

## 5. Contract Tests

عندما توجد Ports/Adapters:
- storage/export/query adapter behavior.
- presentation-facing query contracts عند الحاجة.

## 6. UI / System Tests

عدد محدود لمسارات عالية القيمة:
- login.
- complete Vertical Slice 01.
- finalization.
- server rejection after finalization.

## 7. Human Acceptance

إلزامي قبل اعتبار Slice مكتملًا:

- Desktop.
- Mobile portrait.
- Mobile landscape عند الحاجة.
- RTL.
- وضوح الأفعال والحالات.
- عدم وجود dead ends.
- تقييم بصري وعملي منفصل.

## 8. Regression Rule

كل عيب Domain أو Permission يكتشف في Human Acceptance يجب أن يحصل على automated regression test قبل إغلاقه.

## 9. Architecture Fitness

نراجع دوريًا:
- forbidden cross-module imports/access.
- circular dependencies.
- business logic in presentation.
- direct infrastructure coupling داخل Domain.

يمكن أتمتة بعضها لاحقًا بعد اختيار stack.
