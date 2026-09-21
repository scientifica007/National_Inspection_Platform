# National Inspection Platform

منصة وطنية مرنة لإدارة أعمال التفتيش، صُممت كبداية نظيفة مستقلة عن المشاريع التجريبية السابقة.

## الحالة الحالية

**M0 — Foundation / Domain Design — COMPLETE**

**S01-I01 — Project Skeleton + Identity/Authority Foundation — IMPLEMENTED (بانتظار مراجعة مستقلة)**

الكود موجود الآن على الفرع `build/slice-01`. لم يبدأ أي Increment لاحق.

الحالة المرجعية الحالية:
`docs/PROJECT_STATE.md`

خريطة الوثائق:
`docs/DOCUMENTATION_INDEX.md`

سجل بوابة S01-I01:
`docs/gates/S01-I01_GATE.md`

ملاحظات التنفيذ:
`docs/IMPLEMENTATION_NOTES_S01_I01.md`

## التشغيل المحلي

المتطلبات: Python 3.12 و PostgreSQL.

```bash
# 1) البيئة الافتراضية والاعتماديات
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# 2) إعداد البيئة
cp .env.example .env
# عدّل .env محليًا: DJANGO_SECRET_KEY وبيانات PostgreSQL
# لا تُودِع ملف .env إطلاقًا.

# 3) قاعدة البيانات (PostgreSQL)
sudo -u postgres psql -c "CREATE USER national_inspection WITH PASSWORD 'change-me-local-only' CREATEDB CREATEROLE;"
sudo -u postgres psql -c "CREATE DATABASE national_inspection OWNER national_inspection;"

# 4) الترحيلات والتشغيل
python manage.py migrate
python manage.py createsuperuser   # سينشئ حسابًا وشخصًا مرتبطًا به
python manage.py runserver
```

الفحوصات:

```bash
ruff check .
ruff format --check .
python manage.py check
python manage.py makemigrations --check --dry-run
pytest -q
```

ملاحظة: في اختبارات التكامل قد تحتاج صلاحية إنشاء قاعدة بيانات مؤقتة؛
يُنشئها pytest-django تلقائيًا عند منح المستخدم `CREATEDB`.

## المبادئ المؤسسة

1. **Stable Core** — نواة مفاهيمية صغيرة وثابتة نسبيًا.
2. **Flexible Reality** — الواقع التنظيمي والجغرافي والمهني Data/Configuration كلما أمكن.
3. **Immutable History** — السجلات المثبتة لا يعاد كتابتها؛ التصحيح يضيف تاريخًا.
4. **Progressive Complexity** — لا يضاف تعقيد قبل أن تبرره حاجة حقيقية.
5. **Replaceable Parts** — وحدات وواجهة قابلة للتغيير بحدود وعقود واضحة.
6. **Freedom by Default, Constraint by Rule** — الحرية هي الأصل والقيد يجب أن يكون مبررًا وصريحًا.

## المعمارية

البداية:

**Modular Monolith**

```text
Presentation
    ↓
Application
    ↓
Domain
    ↓
Ports / Infrastructure
```

واجهة المستخدم ليست مصدر قواعد العمل، ويمكن إعادة تصميمها دون إعادة كتابة الـDomain.

## Admin

Admin هو أعلى سلطة إدارية داخل التطبيق، لكن:

**Admin authority ≠ professional authorship**

Admin لا ينتحل هوية مفتش ولا يعيد كتابة سجل مهني مثبت.  
إذا كان Person نفسه يحمل Admin وصلاحية/صفة مهنية، يؤدي الفعل المهني باسمه الحقيقي وفي سياقه المهني.

## منهج التنفيذ

لا تنفيذ كبير دفعة واحدة.

```text
Increment صغير
→ تنفيذ مضبوط
→ تحقق آلي
→ مراجعة مستقلة
→ تصحيح
→ إعادة تحقق
→ Checkpoint
→ Increment تالٍ
```

لا يبدأ Human Acceptance حتى تمر كل Incrementات الـSlice الحالية بهذه الدورة.

## أول تنفيذ

**Vertical Slice 01 — Solo Inspector Field Visit**

ينقسم إلى:

- S01-I01 — Project Skeleton + Identity/Authority Foundation
- S01-I02 — Local Institutions
- S01-I03 — Local Checklist + Versioning
- S01-I04 — Draft Visit + Frozen Snapshot
- S01-I05 — Findings + Recommendations
- S01-I06 — Finalization + Immutability
- S01-I07 — UX/Integration Hardening
- Human Acceptance 01

العمل المصرح به الآن:

**S01-I01 فقط**

## Stack المعتمد

- Python 3.12
- Django 5.2 LTS
- PostgreSQL
- Django Templates
- CSS Design Tokens + reusable components
- minimal JavaScript
- HTMX عند وجود فائدة واضحة فقط
- pytest / pytest-django
- Playwright للمسارات الحرجة
- Ruff
- CI

## تسليم الذكاء الاصطناعي

Executor:
- `docs/AI_EXECUTOR_PROMPT_01.md`
- `docs/AI_EXECUTOR_SPEC_01.md`

Reviewer:
- `docs/AI_REVIEWER_PROMPT_01.md`

الـGate:
- `docs/AI_EXECUTOR_HANDOFF.md`

## الأمان والبيانات

المستودع Public.

ممنوع إدخال:
- بيانات شخصية حقيقية.
- أدلة/وثائق تفتيش سرية.
- production databases.
- tokens / passwords / API keys / secrets.

انظر:
`docs/SECURITY_AND_DATA_GOVERNANCE.md`

## أهم الوثائق

ابدأ من:

1. `docs/DOCUMENTATION_INDEX.md`
2. `docs/PROJECT_STATE.md`
3. `docs/INVARIANTS.md`
4. `docs/PRODUCT_VISION.md`
5. `docs/DOMAIN_MODEL.md`
6. `docs/AUTHORITY_MODEL.md`
7. `docs/ARCHITECTURE_PRINCIPLES.md`
8. `docs/CONTROLLED_IMPLEMENTATION_CYCLE.md`
9. `docs/SLICE_01_INCREMENT_PLAN.md`
10. `docs/AI_EXECUTOR_SPEC_01.md`

## استقلال المشروع

هذا المشروع Clean Slate.

لا يقرأ المنفذ ولا ينسخ ولا يقارن ولا يعمل cherry-pick من المشاريع:
`Inspector_Website_001` … `Inspector_Website_005`
إلا إذا صدر قرار صريح موثق لاحقًا.

## جاهزية الاستخدام

- Design ready for Slice 01: **YES**
- AI executor ready for Slice 01: **YES**
- Human accepted: **NO — not started**
- Pilot ready: **NO**
- Production ready: **NO**
