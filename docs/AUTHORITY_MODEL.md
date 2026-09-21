# Authority Model

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

الصلاحية الفعلية تصور منطقيًا كالتالي:

```text
EffectiveAuthority =
    Capability
    ∩ Scope
    ∩ ValidityPeriod
    ∩ Context
    ∩ DomainInvariants
```

امتلاك Role أو Position لا يتجاوز الـDomain Invariants.

## طبقات السلطة

### System Operator / Developer
طبقة تقنية خارج التسلسل الوظيفي:
- code
- deployment
- backup/restore
- technical configuration

لا تستخدم لتبرير انتحال هوية مستخدم وظيفي، وكل عملية حساسة قابلة للتدقيق تقنيًا.

### Admin
أعلى سلطة داخل التطبيق:
- يرى البيانات ضمن النظام.
- يدير الحسابات والصلاحيات والتهيئة.
- يمكنه إنشاء/إدارة كيانات العمل عندما تسمح الـUse Case.
- لا يستطيع إعادة كتابة سجل مهني مثبت لمستخدم آخر.
- لا يحصل على حق "التصرف باسم شخص آخر" لمجرد كونه Admin.

### Functional Positions
أمثلة:
- Minister
- Inspector General
- Central Inspector
- Field Inspector

هذه Positions/Profiles قابلة للتهيئة وليست if/else صلبة في Domain.

## Capability Grants

Grant نموذجي يحتوي:

- subject: شخص أو Team/Position policy عند الحاجة.
- capability: مثل VIEW, CREATE, ASSIGN, APPROVE, PUBLISH.
- scope: National / Organization / Geography / Team / Institution / Own.
- valid_from / valid_until.
- context optional.
- grant_source.
- delegable: هل يسمح بتفويض جزء منها؟

## Delegation

التفويض:
- لا ينقل هوية المفوض.
- لا يمنح أكثر مما يملك المفوض حق تفويضه.
- يمكن أن يحدد نطاقًا وزمنًا أضيق.
- قابل للإلغاء مع بقاء التاريخ.
- لا يغير author/actor للسجلات الموجودة.

## Ownership vs Visibility vs Authority

هذه ثلاثة أشياء مستقلة:

- **Ownership**: من أنشأ/يمتلك المسودة؟
- **Visibility**: من يستطيع رؤيتها؟
- **Authority**: من يستطيع تنفيذ فعل معين عليها؟

رؤية الكيان لا تعني حق تعديله.

## Inheritance

يمكن أن تمنح المناصب الأعلى Capability set أوسع، لكن:

**Capability inheritance does not imply identity inheritance.**

من ينفذ الفعل يسجل باسمه الحقيقي دائمًا.

## Default policy

- deny by default للعمليات الحساسة.
- least privilege للحسابات العادية.
- freedom by default داخل النطاق الشخصي المشروع للمفتش.
- explicit constraints عندما تكون المهمة أو السياسة مقيدة.
