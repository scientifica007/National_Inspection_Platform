# Domain Invariants

- Status: **Accepted baseline**
- Owner approval: 2026-09-21

هذه القواعد مقصودة لتكون أكثر ثباتًا من الواقع التنظيمي المتغير.

1. **Actor Always Known**  
   كل فعل رسمي أو حساس له فاعل معروف.

2. **Identity Cannot Be Borrowed**  
   امتلاك صلاحية أعلى لا يسمح لشخص بالتصرف وكأنه شخص آخر.

3. **Authority Has Scope**  
   الصلاحية الفعلية تحددها Capability + Scope + Time + Context.

4. **Administrative Power Is Not Professional Authorship**  
   Admin status وحدها لا تمنح حق إنشاء حقيقة مهنية باسم شخص آخر أو إعادة كتابة سجل مهني مثبت.

5. **Draft Is Mutable**  
   المسودات قابلة للتعديل والحذف ضمن الصلاحيات.

6. **Finalized Is Immutable**  
   السجل المثبت لا يعدل تعديلًا هدّامًا ولا يحذف.

7. **Correction Adds History**  
   التصحيح اللاحق يتم كسجل جديد مرتبط بالأصل مع السبب والفاعل والتاريخ.

8. **Relationships May Be Temporal**  
   العضوية والقيادة والانتماء والعمل الجغرافي يمكن أن تكون محددة بزمن.

9. **Historical Meaning Is Frozen**  
   المحتوى الذي استُعمل في تنفيذ موثق يحتفظ بنسخته ودلالته التاريخية.

10. **Data Before Code**  
    الأعداد الحالية، تشكيلات الفرق، التقسيمات، أنواع المحتوى والسياسات المتغيرة تمثل كبيانات/تهيئة عندما لا تكون قانونًا ثابتًا للنظام.

11. **Local Work Must Remain Possible**  
    النظام المركزي لا يمنع العمل المحلي المشروع لمجرد أن كيانًا لم يعتمد وطنيًا بعد.

12. **Sharing Is Explicit**  
    المحتوى المحلي لا يصبح مشتركًا أو عامًا ضمنيًا.

13. **Aggregates Preserve Provenance**  
    كل حصيلة أو مؤشر يجب أن يكون قابلًا للرجوع إلى مصادره ضمن حدود الصلاحيات.

14. **Higher Capability Does Not Rewrite Lower-Level Evidence**  
    الإدارة أو القيادة تستطيع المراجعة والتعليق والتكليف والتجميع، لكنها لا تعيد كتابة معاينة ميدانية مثبتة لصاحبها.

15. **Replaceability Must Not Change Domain Truth**  
    استبدال الواجهة أو التخزين أو آلية الإخراج لا يغير قواعد Domain أو معنى السجلات.

16. **Historical Dependencies Survive Source Retirement**  
    حذف/أرشفة مصدر محلي لا يجوز أن يكسر Snapshot أو سجلًا نهائيًا اعتمد عليه.
