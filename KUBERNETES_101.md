# קוברנטיס 101 — Kubernetes (K8s) Orchestration Foundations

**Module:** `KUBERNETES_101.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — מודול ידע/יסודות תשתית (Knowledge layer, §3 שורה 29).
**Source:** מבוסס על האינפוגרפיקה *"Kubernetes 101"* (Lawal Abdullateef A. · CloudNimbus — DevOps · System Design · Infrastructure).
**Integrates with:** `CLOUD_ARCHITECT_SKILLS.md` (שכבה 4 — Cloud-Native), `AI_SYSTEM_DESIGN.md`, `AI_PROJECT_STRUCTURE.md`, `AI_CLAUDE_STACK_2026.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_HIRING.md`, `CASES/ULEASE_TECH_ONBOARDING.md`

---

> **קוברנטיס בעמוד אחד — היסוד התשתיתי שמתחת לשכבה 4 של ארכיטקט הענן.** `CLOUD_ARCHITECT_SKILLS.md` מזכיר את Kubernetes כ**כלי** בתא אחד (Cloud-Native → Microservices); `AI_SYSTEM_DESIGN.md` עוצר ברמת הרכיב (scaling, תורים, gateway). זה ה**deep-dive** ברמה אחת מתחת: מה K8s פותר, מה החלקים שלו, ו**מתי הוא הכלי הנכון ל-ULease — ומתי הוא over-engineering**. המסגור נאמן לדוקטרינת ה-OS (`CLOUD_ARCHITECT_SKILLS.md` §8, D-046): **חושבים בשכבות ו-trade-offs, לא בכלים** — והשורה התחתונה של המודול היא הכרעת design-review, לא הדרכה טכנית.

## למה מודול — ולמה "101"

עד היום אורקסטרציית קונטיינרים הייתה **פער לא-מתועד** ב-OS: K8s הופיע כשם-כלי ב-`CLOUD_ARCHITECT_SKILLS.md` (שכבה 4) וכרעיון מרומז ב-`AI_SYSTEM_DESIGN.md` (Auto Scaling, Service Discovery, §4.5) — אבל **אף מודול לא מסביר את המנגנון**: Pod, Control Plane, Deployment, Service, HPA. בלי האוריינות הזו, המייסד לא יכול לנהל design-review על השאלה הקריטית ביותר בתשתית — *"כמה תשתית זו יותר מדי תשתית ל-MVP?"*. המודול נותן את 10 אבני-הבניין + טבלת ההכרעה MVP/V1/V2 (§11).

---

## §1 — הבעיה ש-K8s פותר (ולמה זו לא תמיד הבעיה שלך)

ארבע הבעיות שהאינפוגרפיקה מונה — הרצת קונטיינרים ידנית לא סקיילבילית · קונטיינרים קורסים, זזים ומחייבים healing · תנועה צריכה load balancing · אפליקציות צריכות rolling updates בלי downtime. K8s **מאוטמט את כל אלה**.

| הכאב | מה K8s עושה | מתי הכאב הופך אמיתי ל-ULease |
|------|--------------|------------------------------|
| הרצה ידנית לא סקיילבילית | scheduling אוטומטי על פני nodes | כשיש **כמה שירותים** (Ultra·Master·Max + API + workers), לא container בודד |
| קונטיינרים קורסים/זזים | self-healing (restart, reschedule) | כש-uptime הוא **התחייבות חוזית** (SLA 99.5%, D-017) |
| תנועה צריכה איזון | Service + load balancing מובנה | בשיא תנועה (מכרז חי, קמפיין השקה) |
| עדכונים בלי downtime | rolling updates + rollbacks | כשפריסה באמצע היום אסור שתפיל את חדר-העסקה |

> 🛑 **שאלת ה-design-review הנגדית (כלל אנטי-over-engineering, D-037):** אם יש לך **container אחד** ותנועה נמוכה — אין לך אף אחת מ-4 הבעיות. K8s פותר בעיות של **קנה-מידה וריבוי-שירותים**; להריץ אותו לפני שיש לך אותן = להוסיף את הבעיה ה-5 (תשתית מורכבת לתחזוקה) כדי לפתור 4 בעיות שאין לך. ראו §11.

---

## §2 — מושגי הליבה (Cluster · Node · Pod · Container)

| מושג | מה זה | ב-ULease |
|------|-------|----------|
| **Cluster** | Control Plane + worker nodes — יחידת ההרצה | סביבת ה-production המלאה של הפלטפורמה |
| **Node** | מכונה (VM/פיזית) שמריצה workloads | שרת ה-compute (`CLOUD_ARCHITECT_SKILLS.md` שכבה 2) |
| **Pod** | יחידת הפריסה הקטנה ביותר — container אחד או יותר עם IP משותף | מופע של שירות Ultra / Master / API |
| **Container** | חבילת תוכנה קלה ועצמאית | האפליקציה עצמה (Node/Python service, `AI_PROJECT_STRUCTURE.md`) |

> ה-Pod, לא ה-container, הוא יחידת התזמון. כמה containers ב-Pod אחד = sidecar pattern (לוג-שיפר, proxy) — אבל ברירת-המחדל הבריאה: **container אחד ל-Pod**.

---

## §3 — ה-Control Plane (המוח) וה-Data Plane (הידיים)

ה-Control Plane מקבל החלטות גלובליות ושומר על **desired state**; ה-Data Plane (worker nodes) מריץ בפועל.

| רכיב | שכבה | תפקיד | המקבילה ב-OS |
|------|------|--------|---------------|
| **API Server** | Control | שער הכניסה היחיד לאשכול (kubectl/API) | ה-Gateway של `AI_SYSTEM_DESIGN.md` — "דלת אחת" |
| **Scheduler** | Control | מחליט על איזה node ירוץ כל Pod | placement לפי resources (שכבה 2) |
| **Controller Manager** | Control | סוגר את הפער בין רצוי למצוי (reconcile loop) | **דפוס ה-loop** של דוקטרינת Karpathy (D-048) |
| **etcd** | Control | key-value store — מצב האשכול | מקור-אמת אחד למצב (עיקרון הקרנל) |
| **kubelet** | Data | agent על כל node — מנהל containers | — |
| **kube-proxy** | Data | חוקי רשת ל-Pods | — |

> 🎯 **התובנה הארכיטקטונית:** ה-**Controller Manager** הוא בדיוק דפוס ה-*success-criteria + loop* ש-`AI_CLAUDE_STACK_2026.md` §5.7 (דוקטרינת Karpathy, D-048) מתאר: מגדירים **מצב רצוי** (3 replicas), והבקר **מאיטרט עד שמתכנס** — לא רשימת הוראות. אותו עיקרון שמפעיל את ה-eval suite חוסם-ה-deploy (`ULEASE_SPEC.md` §7.2) ואת שערי ה-HITL (D-040).

---

## §4 — Workloads & Objects

| Object | למה | ב-ULease |
|--------|-----|----------|
| **Deployment** | אפליקציות stateless, rolling updates | ה-API, שירותי Ultra·Master (אין מצב מקומי) |
| **StatefulSet** | אפליקציות stateful (DBs) עם זהות יציבה | Postgres/**pgvector** (RAG, §7.1) — או **managed** (מומלץ ל-MVP) |
| **DaemonSet** | Pod אחד לכל node | agents של logging/observability |
| **Job / CronJob** | משימה חד-פעמית / מתוזמנת | **ניקוד באטץ' של לידים** (Haiku), Rank Monitor (GEO), דוח ביקוש שבועי |

> ה-DB ב-StatefulSet הוא אפשרי — אבל ל-ULease, **DB מנוהל** (RDS/Cloud SQL, `CLOUD_ARCHITECT_SKILLS.md` שכבה 2) עדיף עד scale גבוה: פחות שטח-תקיפה תפעולי, גיבוי/replication מובנים. אל תריץ Postgres על K8s רק כי אפשר.

---

## §5 — Networking Basics

כל Pod מקבל **IP משלו**, Pods מתקשרים **בלי NAT**, **Service** חושף Pods (פנימית/חיצונית), **Ingress** מנהל ניתוב HTTP/HTTPS.

- **Service** = כתובת יציבה מול קבוצת Pods מתחלפת (מפשט את ה-Service Discovery של `AI_SYSTEM_DESIGN.md` §4.5).
- **Ingress** = שכבת ה-routing/TLS בכניסה — המקבילה ל-API Gateway + reverse proxy (`AI_SYSTEM_DESIGN.md` שער הכניסה).

> 🎯 **ב-ULease:** Ingress הוא הנקודה שבה `Leasing.co.il` ↔ `ULease.co.il` נכנסים; ה-Service מבטיח שמופע Ultra שקרס והוחלף **לא מנתק** את חדר-העסקה — הצרכן לא יודע שמשהו זז.

---

## §6 — Configuration & Secrets

**ConfigMap** מאחסן קונפיגורציה · **Secret** מאחסן דאטה רגישה · שניהם מותקנים כקבצים או env vars.

> 🎯 **ב-ULease (גבול ציות):** מפתחות API (יבואנים, מימון, Claude), חיבורי DB ו-tokens חיים ב-**Secrets** — לא בקוד, לא ב-repo. זו נקודת המפגש עם שכבה 3 של `CLOUD_ARCHITECT_SKILLS.md` (secrets/Vault) ועם **Guardian** (PII/תשלומים, D-016). הערה: Secret של K8s הוא base64, **לא הצפנה** — ל-production צריך encryption-at-rest / external secrets manager (פריט design-review).

---

## §7 — Scaling & Resilience

**ReplicaSet** מבטיח מספר Pods רצוי · **HPA** (Horizontal Pod Autoscaler) מסקיל אוטומטית · self-healing ע"י restart/reschedule · **rolling updates ו-rollbacks** מובנים.

| יכולת | מה היא נותנת ל-SLA של ULease (D-017) |
|--------|--------------------------------------|
| ReplicaSet | אין נקודת-כשל יחידה — תמיד ≥N מופעים |
| HPA | uptime 99.5% גם בשיא מכרז/קמפיין |
| self-healing | "ליד ≤1h" שורד קריסת Pod בלי התערבות |
| rolling update / rollback | פריסה באמצע יום עסקים — ואם נשבר, **חזרה אחורה בפקודה אחת** |

> 🎯 משלים את ה-**Circuit Breaker** של `AI_SYSTEM_DESIGN.md` §4.5 (API של יבואן נופל ≠ הפלטפורמה נופלת): K8s מטפל בכשל **שלך** (Pod), ה-Circuit Breaker בכשל **של התלות החיצונית**.

---

## §8 — Observability & Ops

health checks (**liveness** = חי? · **readiness** = מוכן לתנועה?) · logs ו-metrics · אינטגרציית monitoring/alerting · ניהול **declarative** של מצב רצוי.

> 🎯 **ב-ULease:** ה-health checks הם המקבילה התשתיתית ל-**eval suite** (`ULEASE_SPEC.md` §7.2, D-023) — liveness/readiness בודקים שה-Pod *רץ*, evals בודקים שהסוכן *נכון* (grounding 100%). שניהם חוסמים תנועה למופע לא-תקין. ה-alerting מתחבר ישירות לשכבה 5 של `CLOUD_ARCHITECT_SKILLS.md` (Observability/**SLOs**) ולהתראות BI (`AI_DATA_BI.md` §6.ד: "ליד ממתין > שעה").

---

## §9 — Security Basics

**Namespaces** לבידוד · **RBAC** לבקרת גישה · **Pod Security & securityContext** · **Network Policies** לבקרת תנועה.

| בקרה | ב-ULease |
|------|----------|
| **Namespaces** | בידוד סביבות (dev/staging/prod) ו/או הפרדת שירותים |
| **RBAC** | least-privilege — מי ניגש למה (תאום ל-IAM, `CLOUD_ARCHITECT_SKILLS.md` שכבה 3) |
| **securityContext** | container לא רץ כ-root — hardening בסיסי |
| **Network Policies** | מי מדבר עם מי — ה-DB לא חשוף לכל Pod |

> 🎯 בידוד הוא עקרון חוצה-OS: **Namespaces/RBAC** ברמת התשתית = המקבילה ל-**RLS** ברמת הדאטה (`AI_DATA_BI.md` §6, ספק רואה רק את שלו) ול-**JWT/RLS** ברמת ה-API (`AI_SYSTEM_DESIGN.md` §4). זו אותה דרישת multi-tenant, בשלוש שכבות — ומנדט מובהק ל-Tech Lead (4 ה-🟡 ב-`AI_PROFICIENCIES_2026.md`, שכבה 3 ב-`CLOUD_ARCHITECT_SKILLS.md`).

---

## §10 — איך K8s מתחבר ל-DevOps

מאפשר CI/CD · תומך ב-**GitOps** · מתקנן פריסות בין סביבות · מניע פלטפורמות cloud-native מודרניות.

> 🎯 **ב-ULease:** ה-**CI חוסם-merge כבר קיים** (`os-consistency.yml`, D-023) — זה ה-*CI*. ה-*CD* וה-**GitOps** (מצב הרצוי חי ב-Git, Argo CD מסנכרן — `CLOUD_ARCHITECT_SKILLS.md` שכבה 4) הם הצעד הבא, מנדט Tech Lead. ה-declarative של K8s תאום מושלם לדוקטרינת ה-OS: **מתארים מצב רצוי, לא רצף פעולות** — בדיוק כמו `CLAUDE.md` שמתאר את ה-OS ולא סקריפט אתחול.

---

## §11 — הכרעת design-review: מתי K8s ל-ULease (ומתי לא)

הלב של המודול. K8s **לא דרישת MVP** — הוא תשובה לבעיות שמגיעות עם scale. שלב לפי בשלות, לא לפי יוקרה:

| שלב | תשתית הרצה | למה |
|------|-------------|-----|
| **MVP** (היום) | **Managed platform** (App Service / Cloud Run / Fly.io) — בלי K8s | שירות-שניים, תנועה נמוכה, צוות של 1. K8s = overhead תפעולי שלא מחזיר ערך. ה-admin console רץ מלפטופ במשרד ספק (D-045) — לא צריך אשכול בשביל זה. |
| **V1** (ריבוי שירותים) | **Managed K8s** (EKS/GKE/AKS) כש-Ultra·Master·Max נפרסים כשירותים מתוזמרים נפרדים | כשמופיעות הבעיות של §1: ריבוי שירותים, HPA אמיתי, rolling updates יומיים, SLA חוזי |
| **V2** (scale/enterprise) | K8s מלא + service mesh + GitOps + policy-as-code | multi-region, service mesh (Istio), FinOps (Kubecost) — שכבות 4–5 של `CLOUD_ARCHITECT_SKILLS.md` |

> 🚦 **שער המעבר (אנטי-over-engineering, תאום ל-D-037 ו-`AI_PROJECT_STRUCTURE.md` §3.2):** אַמֵּץ K8s רק כשמתקיים **לפחות אחד**: (א) ≥3 שירותים עצמאיים שצריך לתזמר · (ב) HPA נדרש בפועל (תנועה תנודתית מוכחת) · (ג) rolling updates בלי downtime הפכו לדרישה חוזית · (ד) הצוות גדל מעבר למפתח בודד. עד אז — **managed platform**. אותה דוקטרינה כמו "סוכן שני / API חיצוני / Guardian" כשערי-מעבר ב-`AI_PROJECT_STRUCTURE.md`.

> 🎯 **כשאלת ראיון ל-Tech Lead** (משלים את `CASES/ULEASE_HIRING.md` §ו ואת רובריקת `CLOUD_ARCHITECT_SKILLS.md` §6, שכבה 4): מועמד שמתחיל מ-*"נקים Kubernetes"* ל-MVP של שירות-בודד נמצא ב-🔴 (over-engineering, "6 חודשים ל-MVP"); מועמד 🟢 שואל קודם *"כמה שירותים, איזו תנועה, איזה SLA"* — ורק אז בוחר. **חושב בשכבות, לא בכלים** (D-046).

---

## §12 — השורה התחתונה

Kubernetes הוא **אמצעי** (reliability, scale, self-healing) — לא מטרה. ב-production אף אחד לא שואל אם הרצת על K8s; שואלים אם המערכת **scales, survives ו-cost-efficient** (`CLOUD_ARCHITECT_SKILLS.md` §8). ל-ULease המסר כפול: (1) **המנגנונים** של K8s — desired-state reconciliation, self-healing, declarative ops — הם תאומים תשתיתיים לעקרונות שכבר מפעילים את ה-OS (loop, eval-gates, מקור-אמת אחד); (2) **התזמון** של אימוצו הוא מבחן בגרות הנדסי — מנצחים עם הארכיטקטורה הנכונה לשלב, לא עם התשתית המרשימה ביותר (D-046). אל תאמץ K8s כדי להיראות רציני; אמץ אותו כשהבעיות של §1 אמיתיות.

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | יצירת המודול — 10 אבני-הבניין של Kubernetes (בעיה · מושגי ליבה · Control/Data Plane · Workloads · Networking · Config/Secrets · Scaling · Observability · Security · DevOps) + §11 הכרעת design-review MVP/V1/V2 ושער אנטי-over-engineering + §12 השורה התחתונה. ממופה ל-ULease ולדוקטרינת "שכבות לא כלים". מבוסס אינפוגרפיקת *"Kubernetes 101"* (Lawal Abdullateef A. · CloudNimbus) — D-061 | 2026-06-04 |

**Attribution.** מבנה 10 הסעיפים והמושגים: האינפוגרפיקה *"Kubernetes 101"* (Lawal Abdullateef A. · CloudNimbus — DevOps · System Design · Infrastructure). המיפוי ל-ULease, הכרעת ה-design-review ושער האנטי-over-engineering — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of KUBERNETES_101.md v1.0.0 —*
