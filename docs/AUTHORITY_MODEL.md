# Authority Model

- Status: **Accepted for initial implementation**
- Owner approval: 2026-09-21

## الهدف

بناء صلاحيات مرنة تسمح بالتغيير التنظيمي والعمل الفردي والجماعي من دون تحويل الرتب إلى قيود صلبة في الكود.

## الفصل الأساسي

- **Person**: من هو الإنسان؟
- **Position**: ما صفته الرسمية/المهنية؟
- **Operational Role**: ما دوره في هذا الفريق أو هذه المهمة؟
- **Capability**: ما الفعل الذي يمكنه القيام به؟
- **Scope**: على أي نطاق؟
- **Time**: خلال أي مدة؟
- **Context**: ضمن أي فريق/مهمة/وحدة؟

## قاعدة التقييم

```text
EffectiveAuthority =
    Capability
    ∩ Scope
    ∩ ValidityPeriod
    ∩ Context
    ∩ DomainInvariants
```

امتلاك Role أو Position أو Admin status لا يتجاوز Domain Invariants.

## Scope semantics

Scope قيمة دلالية وليست نصًا اعتباطيًا.

أمثلة مستقبلية:

```text
OWN
NATIONAL
ORGANIZATION(id)
GEOGRAPHY(id)
TEAM(id)
INSTITUTION(id)
MISSION(id)
```

إذا انطبق أكثر من قيد على Grant واحد فالمعنى الافتراضي هو **التقاطع**.

مثال:
```text
GEOGRAPHY(Tébessa) ∩ TEAM(A)
```
يعني عناصر Team A الواقعة داخل نطاق تبسة.

الـUnion يحتاج Grants منفصلة أو Policy صريحة؛ لا يستنتج تلقائيًا.

في Vertical Slice 01 ننفذ فقط OWN وALL لتقليل التعقيد.

## طبقات السلطة

### System Operator / Developer
طبقة تقنية خارج التسلسل الوظيفي:
- code
- deployment
- backup/restore
- technical configuration

لا تستخدم لتبرير انتحال هوية مستخدم وظيفي، وكل عملية حساسة قابلة للتدقيق تقنيًا.

### Admin
أعلى سلطة إدارية داخل التطبيق:
- يرى بيانات التطبيق وفق السياسة الإدارية العامة.
- يدير الحسابات والصلاحيات والتهيئة.
- ينشئ/يدير كيانات العمل عندما تسمح Use Case.
- لاحقًا يستطيع إنشاء Missions ونشرها أو تكليف المؤهلين.
- لا يعيد كتابة سجل مهني مثبت.
- لا يحصل على حق التصرف باسم شخص آخر.
- Admin status وحدها ليست Professional Capability.

قد يكون Person نفسه Admin ومفتشًا/وزيرًا/صاحب Position مهنية. عند تنفيذ فعل مهني يسجل الفعل باسمه الحقيقي وبالسياق المهني المستخدم.

### Functional Positions
أمثلة:
- Minister
- Inspector General
- Central Inspector
- Field Inspector

هذه Positions/Profiles قابلة للتهيئة وليست if/else صلبة في Domain.

يمكن لسياسة المنصة منح Position أعلى مجموعة Professional Capabilities تشمل ما يحتاجه من أعمال المستويات الأدنى، من دون استعارة هوية أي شخص آخر.

## Capability Grants

Grant نموذجي يحتوي:
- subject.
- capability.
- scope.
- valid_from / valid_until.
- context optional.
- grant_source.
- delegable.

## Delegation

التفويض:
- لا ينقل هوية المفوض.
- لا يمنح أكثر مما يملك المفوض حق تفويضه.
- يمكن أن يحدد نطاقًا وزمنًا أضيق.
- قابل للإلغاء مع بقاء التاريخ.
- لا يغير author/actor للسجلات الموجودة.

## Ownership vs Visibility vs Authority

- **Ownership**: من أنشأ/يمتلك المسودة؟
- **Visibility**: من يستطيع رؤيتها؟
- **Authority**: من يستطيع تنفيذ فعل معين عليها؟

الرؤية لا تعني حق التعديل.

## Inheritance

**Capability inheritance does not imply identity inheritance.**

من ينفذ الفعل يسجل باسمه الحقيقي دائمًا.

## Default policy

- deny by default للعمليات الحساسة.
- least privilege للحسابات العادية.
- freedom by default داخل النطاق الشخصي المشروع للمفتش.
- explicit constraints عندما تكون المهمة أو السياسة مقيدة.
