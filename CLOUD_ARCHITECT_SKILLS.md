# כישורי ארכיטקט ענן — The Key Cloud Architect Skills

**Module:** `CLOUD_ARCHITECT_SKILLS.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/מפת-כישורים (Knowledge layer).
**Source:** מבוסס על האינפוגרפיקה *"The Key Cloud Architect Skills — Complete Mastery Guide"* (Alok Sharan).
**Integrates with:** `CASES/ULEASE_HIRING.md`, `CASES/ULEASE_TECH_ONBOARDING.md`, `AI_ROLES_2026.md`, `AI_SKILL_MAP.md`, `AI_SYSTEM_DESIGN.md`, `AI_DATA_BI.md`, `CASES/ULEASE_SPEC.md`

---

> **מפת חמש שכבות לכישורי ארכיטקט ענן — הציר שהיה חסר.** `AI_SKILL_MAP.md` ממפה את ציר ה-**AI** (Tools→Workflows→Agentic→Architect); זה הציר המשלים — **תשתית הענן**. התזה: ארכיטקט חזק לא חושב **כלים** (AWS/Azure/GCP), אלא **שכבות, trade-offs והתנהגות מערכת לאורך זמן**. שני שימושים ב-ULease: (1) **רובריקת כשירות וראיון** ל-Tech Lead — משלימה את `ULEASE_HIRING.md` שיש בו תפקיד אך לא סולם מדורג; (2) **אוריינות design-review** למייסד.

## למה מודול ולא הערה ב-HIRING

עד היום שכבת ה-Security & Governance, ה-IaC (Terraform), ה-FinOps וה-SLOs היו **פערים לא-מתועדים** ב-OS. `ULEASE_HIRING.md` מזכיר "Cloud/hosting, CI/CD, אבטחה" בפרוזה, אך בלי **מדרגה** (מה נחשב Beginner מול Advanced). המודול הזה נותן את הסולם המדורג — לכל תת-תחום: Beginner / Intermediate / Advanced + Tools + Time — וממפה כל שכבה ל-ULease.

---

## שכבה 1 — Foundation Cloud Skills

> ידע הליבה שצריך **לפני** שמתכננים מערכות ענן. אם השכבה הזו חלשה — כל החלטה מעליה היא ניחוש.

| תת-תחום | Beginner | Intermediate | Advanced | Tools | Time |
|----------|----------|--------------|----------|-------|------|
| **Cloud Fundamentals** | מודלי ענן, regions, שירותי בסיס | מיפוי workloads, בחירת שירות | חשיבה multi-cloud, architecture trade-offs | AWS · Azure · GCP | 2ח' |
| **Networking Basics** | VPC, subnets, DNS, routing | Load balancers, VPNs, firewalls | hybrid networking, private connectivity | AWS VPC · Azure VNet · Cloudflare | 3ח' |
| **Linux & Servers** | shell, קבצים, users, processes | SSH, logs, הרשאות | hardening, אוטומציה, tuning | Linux · Bash · Ubuntu | 2ח' |

🎯 **ב-ULease:** הרצפה שעליה רץ הכל — hosting ‏`Leasing.co.il` ↔ `ULease.co.il`, ה-admin console שעובד מלפטופ במשרד ספק (D-045). אחריות ישירה של ה-Tech Lead (`ULEASE_HIRING.md` §ב).

---

## שכבה 2 — Cloud Infrastructure Design

> איך מתכננים compute, storage ו-database סקיילביליים. אלו לא "שירותים" — אלו **החלטות עיצוב** שמשפיעות ישירות על scalability, עלות וביצועים.

| תת-תחום | Beginner | Intermediate | Advanced | Tools | Time |
|----------|----------|--------------|----------|-------|------|
| **Compute** | VMs, containers, serverless | autoscaling, instance sizing | capacity planning, workload placement | EC2 · Azure VM · Lambda | 3ח' |
| **Storage** | object, block, file | backup, replication, lifecycle | DR, compliance storage | S3 · Azure Blob · GCS | 2ח' |
| **Databases** | SQL, NoSQL, managed | indexing, backups, replication | sharding, failover, multi-region | RDS · DynamoDB · Cosmos DB | 3ח' |

🎯 **ב-ULease:** כאן חיים הקטלוג, המלאי ודאטת העסקאות; **pgvector** ל-RAG (`ULEASE_SPEC.md` §7.1), Elasticsearch לחיפוש רכב (D-037). הבית הקנוני להעמקה: `AI_SYSTEM_DESIGN.md` (מפת הרכיבים) + `AI_DATA_BI.md` (star schema) + `ULEASE_SPEC.md` §8.

---

## שכבה 3 — Cloud Security & Governance

> איך מגנים על זהויות, דאטה, workloads וסביבות. אבטחה היא **לא שכבה נפרדת** — היא מוטמעת ב-identity, access, logging וציות מיום 1.

| תת-תחום | Beginner | Intermediate | Advanced | Tools | Time |
|----------|----------|--------------|----------|-------|------|
| **Identity & Access** | users, roles, permissions | least privilege, access reviews | **zero trust**, federated identity | IAM · Azure AD · Google IAM | 3ח' |
| **Security Controls** | הצפנה, secrets, logging | threat detection, vuln scanning | incident response, risk modeling | GuardDuty · Defender · Vault | 4ח' |
| **Governance** | tags, budgets, policies | compliance checks, resource controls | **landing zones**, policy automation | AWS Organizations · Azure Policy · Terraform | 4ח' |

🎯 **ב-ULease:** PII ותשלומים (שאלת ראיון `ULEASE_HIRING.md` §ו3), **Guardian** (ציות, opt-out, audit — D-016), KYC. zero trust / landing zones = V1+. **השכבה שה-OS הכי פחות כיסה — עכשיו יש לה בית.**

---

## שכבה 4 — Cloud-Native Architecture

> איך אפליקציות ענן מודרניות נבנות, מופצות ומתוזמרות. כאן מערכות הופכות גמישות, עמידות ו-production-ready.

| תת-תחום | Beginner | Intermediate | Advanced | Tools | Time |
|----------|----------|--------------|----------|-------|------|
| **Microservices** | APIs, services, containers | API gateways, service discovery | **service mesh**, resilience patterns | Kubernetes · Docker · Istio | 4ח' |
| **DevOps & CI/CD** | Git, pipelines, deployments | testing, releases, rollbacks | **GitOps**, progressive delivery | GitHub Actions · Jenkins · Argo CD | 3ח' |
| **Infrastructure as Code** | infra templates | modules, environments, state | **policy-as-code**, drift detection | Terraform · Pulumi · CloudFormation | 3ח' |

🎯 **ב-ULease:** מנוע Ultra·Master·Max כשירותים מתוזמרים; **CI חוסם-merge** כבר קיים (D-023); **IaC (Terraform) = חדש לפלטפורמה**. הבית הקנוני: `AI_SYSTEM_DESIGN.md` §1.5 (מסלול הבקשה השכבתי) + `AI_PROJECT_STRUCTURE.md` + `AI_CLAUDE_STACK_2026.md`.

---

## שכבה 5 — Reliability, Cost & Advanced Architecture

> איך שומרים מערכות ענן יציבות, יעילות ומוכנות ל-enterprise scale. בקנה-מידה, ארכיטקטורה היא **trade-offs**: reliability מול cost, performance מול complexity, speed מול governance.

| תת-תחום | Beginner | Intermediate | Advanced | Tools | Time |
|----------|----------|--------------|----------|-------|------|
| **Reliability & Observability** | logs, metrics, alerts | tracing, **SLOs**, failover | multi-region, incident automation | CloudWatch · Grafana · Datadog · OpenTelemetry | 4ח' |
| **Cost Optimization** | budgets, billing alerts | rightsizing, reserved instances | **FinOps**, chargeback models | Cost Explorer · Kubecost · Azure Cost Mgmt | 3ח' |
| **Enterprise Architecture** | requirements, diagrams | trade-offs, migration planning | AI infrastructure, multi-cloud strategy | Well-Architected Tool · Azure Migrate · Databricks · Snowflake | 6+ח' |

🎯 **ב-ULease:** observability/SLOs = ניטור ה-eval suite (`ULEASE_SPEC.md` §7.2); **FinOps** = cost-per-query (D-022) + `AI_RAG_DESIGN.md` #15 + יחידת הכלכלה (`INVESTOR_RELATIONS.md`); Enterprise = הסיפור למשקיע ("מנצחים עם הארכיטקטורה, לא עם המודל הגדול", D-046).

---

## §6 — רובריקת הכשירות ל-Tech Lead (סולם ראיון)

חמש השכבות הופכות את שאלות הראיון ב-`ULEASE_HIRING.md` §ו לסולם מדורג. לכל שכבה — מה **חובה ל-MVP** מול **V1+**, ומה מבדיל תשובת Beginner מ-Advanced:

| שכבה | חובה ל-MVP | V1+ | סימן ל-Advanced (🟢) |
|------|-----------|-----|----------------------|
| 1 Foundation | hosting + Linux + networking בסיסי | hybrid/private connectivity | מדבר trade-offs בין regions/ספקים, לא רק "מכיר AWS" |
| 2 Infra Design | compute+DB מנוהל, pgvector | sharding, multi-region | בוחר instance/DB לפי workload, לא לפי הרגל |
| 3 Security | הצפנה, IAM, secrets, PII/תשלומים | zero trust, landing zones | אבטחה "by design", לא "נוסיף בסוף" |
| 4 Cloud-Native | CI/CD, containers, IaC בסיסי | service mesh, GitOps | policy-as-code + drift detection |
| 5 Reliability/Cost | logs/metrics/alerts, תקציבי עלות | SLOs, FinOps, incident automation | מדבר reliability-מול-cost כ-trade-off מפורש |

> **חיבור לדגלים (`ULEASE_HIRING.md` §ו):** 🟢 "מדבר trade-offs" ו-🔴 "over-engineering / 6 חודשים ל-MVP" הם בדיוק התזה של המפה הזו — **חושב בשכבות, לא בכלים**. מועמד שמתחיל מ"איזה שירות" במקום מ"איזו דרישה" — נמצא ב-Beginner של שכבה 5 (Enterprise Architecture).

---

## §7 — בגרות ULease מול חמש השכבות (תמונת מצב ל-design review)

| שכבה | סטטוס ב-ULease | הפער לסגירה |
|------|----------------|--------------|
| 1 Foundation | 🟢 מתוכנן (hosting, admin console D-045) | — |
| 2 Infra Design | 🟢 מאופיין (`AI_SYSTEM_DESIGN` · `AI_DATA_BI` · SPEC §8) | multi-region = scale |
| 3 Security & Governance | 🟡 חלקי (Guardian, ציות D-016) | **IAM/zero trust/landing zones — הפער הגדול ל-Go-Live** |
| 4 Cloud-Native | 🟡 חלקי (CI D-023, פייפליין §1.5) | **IaC/Terraform — חדש**; service mesh = scale |
| 5 Reliability/Cost | 🟡 חלקי (evals §7.2, cost-per-query D-022) | SLOs פורמליים, FinOps/chargeback |

> שתי השכבות עם הפער הגדול ביותר ל-Go-Live: **3 (Security)** ו-**4 (IaC)** — שתיהן מנדט מובהק ל-Tech Lead ב-Phase 0. מאמת את `AI_PROFICIENCIES_2026` (4 ה-🟡 = מנדט ה-Tech Lead).

---

## §8 — השורה התחתונה

הכלים מתחלפים כל שנה; **חשיבה ארכיטקטונית מצטברת לאורך זמן.** המטרה אינה ללמוד AWS/Azure/GCP בנפרד — אלא להבין איך מערכות מתנהגות תחת לחץ אמיתי. ב-production אף אחד לא שואל באיזה שירות השתמשת; שואלים אם המערכת **scales, survives, ונשארת cost-efficient**. זו אותה דוקטרינה כמו `AGENT_BLUEPRINT.md` (מערכת, לא מודל) ו-D-046 (ארכיטקטורה, לא המודל הגדול).

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | יצירת המודול — 5 שכבות כישורי ארכיטקט ענן (Foundation→Enterprise) עם מדרגת Beginner/Intermediate/Advanced + Tools + Time, רובריקת ראיון ל-Tech Lead (§6), תמונת בגרות ULease (§7) ומיפוי לבית הקנוני בכל שכבה. מבוסס אינפוגרפיקת *"The Key Cloud Architect Skills"* (D-057) | 2026-06-04 |

**Attribution.** מבנה 5 השכבות והמדרגות: האינפוגרפיקה *"The Key Cloud Architect Skills — Complete Mastery Guide"* (Alok Sharan). המיפוי ל-ULease, רובריקת הראיון ותמונת הבגרות — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of CLOUD_ARCHITECT_SKILLS.md v1.0.0 —*
