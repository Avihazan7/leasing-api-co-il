# קוברנטיס 101 — Kubernetes 101 (תזמור קונטיינרים)

**Module:** `KUBERNETES_101.md`
**Version:** 1.0.0
**Author:** Avraham Bar Yochai Chazan — Claude Operating System
**Status:** Active — Knowledge layer (§3 שורה 30). מודול התשתית/DevOps — תזמור קונטיינרים; ה-deep-dive של שכבת ה-Cloud-Native ב-`CLOUD_ARCHITECT_SKILLS` §4.
**Source:** מבוסס על האינפוגרפיקה *"Kubernetes 101"* (Lawal Abdullateef A. / CloudNimbus) + פירוט 10 הסעיפים.
**Integrates with:** `CLOUD_ARCHITECT_SKILLS.md` (§4 Cloud-Native), `AI_SYSTEM_DESIGN.md`, `AI_PROJECT_STRUCTURE.md`, `AI_CLAUDE_STACK_2026.md`, `CASES/ULEASE_SPEC.md`, `CASES/ULEASE_TECH_ONBOARDING.md`, `CASES/ULEASE_HIRING.md`

---

> **Kubernetes (K8s) = מערכת ההפעלה של הקונטיינרים** — מתזמרת deployment, scaling וניהול של אפליקציות מכולתיות (containerized). המודול מזקק את "K8s 101" וממפה אותו ל-ULease — אבל עם דגל ברור: **ה-MVP של ULease רץ על `docker-compose`, לא על K8s** (`leasing-api/docs/specs/deployment-and-launch.md`). K8s הוא הכרעת **V1+**. לכן זה לא מדריך הקמה — זו **אוריינות design-review** שמאפשרת למייסד לשאול את ה-Tech Lead *מתי* ו*אם* לעבור אליו, בלי לכתוב YAML.

## למה מודול ולא הערה ב-CLOUD_ARCHITECT_SKILLS

עד היום K8s היה **שם-כלי בתא אחד** ב-`CLOUD_ARCHITECT_SKILLS.md` §4 (Cloud-Native → Microservices → "Kubernetes · Docker · Istio") — מפת-כישורים מדורגת, לא explainer; ו-`AI_SYSTEM_DESIGN.md` לא נגע בתזמור קונטיינרים כלל. זהו הבית הקנוני שחסר: ה-**deep-dive** של תזמור הקונטיינרים, המשלים את מפת הכישורים (איזה כלי) במפת ה**מושגים** (איך הוא עובד ולמה).

---

## 1. הבעיה ש-K8s פותר

| בלי K8s | מה K8s עושה |
|----------|--------------|
| הרצת קונטיינרים ידנית לא סקיילבילית | תזמור אוטומטי של עשרות/מאות קונטיינרים |
| קונטיינרים קורסים, זזים, צריכים החלמה | **self-healing** — restart/reschedule אוטומטי |
| תעבורה צריכה איזון עומסים | Service + load balancing מובנה |
| עדכונים בלי downtime | **rolling updates** + rollback מובנים |

> **ב-ULease:** ב-MVP (שירות בודד, עומס נמוך) ארבעת הכאבים האלה קטנים — `docker-compose` מספיק. הסימן לעבור ל-K8s: ריבוי שירותים (Ultra·Master·Max כשירותים נפרדים), צורך ב-autoscaling אמיתי, או SLA uptime (99.5%, D-017) שדורש self-healing מנוהל.

---

## 2. מושגי הליבה

| מושג | מה זה | ב-ULease |
|------|--------|-----------|
| **Cluster** | Control Plane + Worker Nodes | סביבת ה-production כולה |
| **Node** | מכונה (VM/פיזית) שמריצה workloads | EC2/VM אצל ספק הענן |
| **Pod** | היחידה הקטנה ביותר לפריסה — קונטיינר אחד או יותר | מופע של ה-API / סוכן |
| **Container** | חבילה שמריצה את האפליקציה | ה-image של שירות ULease |

---

## 3. הארכיטקטורה — Control Plane מול Worker Node

האינפוגרפיקה בנויה סביב שני המישורים. זה הלב:

**Control Plane (Master Node)** — מנהל את מצב הקלאסטר ומקבל החלטות גלובליות:

| רכיב | תפקיד |
|------|--------|
| **API Server** | שער הכניסה היחיד לקלאסטר (kubectl / API / Dashboard עוברים דרכו) |
| **etcd** | key-value store מבוזר — **מצב הקלאסטר** (מקור האמת) |
| **Scheduler** | מחליט על איזה Node ירוץ כל Pod (לפי משאבים זמינים) |
| **Controller Manager** | שומר על ה-desired state של אובייקטי הקלאסטר |
| **Cloud Controller Manager** | אינטגרציה עם ה-API של ספק הענן (LB, storage, nodes) |

**Worker Node (Data Plane)** — מארח Pods ומריץ את ה-workloads:

| רכיב | תפקיד |
|------|--------|
| **kubelet** | הסוכן על כל Node — מנהל קונטיינרים ו-Pods, מדבר עם ה-API Server (gRPC) |
| **Container Runtime** | מריץ את הקונטיינרים בפועל; **CRI shim** מתרגם קריאות K8s ל-runtime |
| **kube-proxy** | מתחזק את חוקי הרשת ל-Pods (ניתוב Service) |

> **אזהרת בלבול שמות:** "Control Plane" כאן = ה-master node של K8s. ב-ULease "Control Plane" מתאר לעיתים את שכבת התזמור של **Ultra** (`ULEASE_SPEC.md` §7). שתי שכבות שונות לחלוטין — אל תערבב בין תזמור-קונטיינרים לתזמור-סוכנים.

---

## 4. Workloads & Objects

| אובייקט | תפקיד | המקבילה ב-ULease |
|---------|--------|-------------------|
| **Deployment** | אפליקציות stateless + rolling updates | ה-API, מנוע הסוכנים (חסרי-מצב) |
| **ReplicaSet** | שומר על מספר Pods יציב (מנוהל ע"י Deployment) | רפליקות של ה-API |
| **StatefulSet** | אפליקציות stateful (DBs) | PostgreSQL/pgvector — **או** DB מנוהל (מומלץ ל-MVP) |
| **DaemonSet** | Pod אחד לכל Node | agents של logging/monitoring |
| **Job / CronJob** | משימה חד-פעמית / מתוזמנת | batch: רענון מלאי, דוח ביקוש שבועי (`AI_DATA_BI` §6.ד) |

---

## 5. רשת (Networking)

- כל **Pod** מקבל IP משלו; Pods מתקשרים ביניהם **בלי NAT**.
- **Service** — מפשט גישה ל-Pods (פנימית/חיצונית), עם load balancing.
- **Ingress** — ניתוב HTTP/HTTPS חיצוני.

> **ב-ULease:** ה-Ingress הוא נקודת ה-HTTPS של `Leasing.co.il` ↔ `ULease.co.il`; ה-Service מפשט את הגישה לשירותי ה-backend (`AI_SYSTEM_DESIGN.md` — ה-gateway/API styles שזה מממש).

---

## 6. Configuration & Secrets

- **ConfigMap** — קונפיגורציה לא-רגישה.
- **Secret** — דאטה רגישה (מפתחות API, סיסמאות DB, מפתח Claude API).
- שניהם מוזרקים כקבצים או כ-environment variables.

> **ב-ULease:** ה-Secrets הם מפתח ה-Claude API, פרטי ה-DB, ומפתחות ספקי המימון/ביטוח — מתחבר לשכבת Security (§9) ול-Guardian (D-016).

---

## 7. Scaling & Resilience

| יכולת | מה זה | ב-ULease |
|--------|--------|-----------|
| **ReplicaSet** | מבטיח את מספר ה-Pods הרצוי | זמינות בסיסית |
| **HPA** (Horizontal Pod Autoscaler) | מגדיל/מקטין Pods אוטומטית לפי עומס | פיקים בתעבורה (קמפיין ההשקה) |
| **Self-healing** | restart/reschedule אוטומטי | תמיכה ב-SLA uptime 99.5% (D-017) |
| **Rolling updates / rollback** | פריסה בלי downtime + חזרה לאחור | deploy של גרסה חדשה בלי להפיל את הפלטפורמה |

---

## 8. Observability & Ops

- **Health checks**: liveness (חי?) + readiness (מוכן לתעבורה?).
- **Logs & metrics**, אינטגרציית monitoring/alerting.
- ניהול **declarative** של ה-desired state (`kubectl apply`, לא פקודות imperative).

> **ב-ULease:** מתחבר ל-eval suite + ניטור ה-production (`ULEASE_SPEC.md` §7.2) ול-SLOs (שכבה 5 ב-`CLOUD_ARCHITECT_SKILLS`). ה-readiness probe הוא מה שמונע ניתוב תעבורה ל-Pod שעדיין לא טען את המודל/החיבורים.

---

## 9. Security

| בקרה | מה זה | ב-ULease |
|------|--------|-----------|
| **Namespaces** | בידוד לוגי בתוך קלאסטר | הפרדת סביבות / רכיבים |
| **RBAC** | בקרת גישה מבוססת-תפקיד | מקביל ל-RLS של M9 (`AI_DATA_BI` §6.ב) — least privilege |
| **securityContext / Pod Security** | הקשחת הרשאות הקונטיינר | אבטחה "by design" (שכבה 3, `CLOUD_ARCHITECT_SKILLS`) |
| **Network Policies** | בקרת תעבורה בין Pods | בידוד רב-דיירותי, מניעת lateral movement |

> אבטחה ב-K8s היא **לא שכבה שמוסיפים בסוף** — בדיוק התזה של שכבה 3 ב-`CLOUD_ARCHITECT_SKILLS` (🟢 "by design").

---

## 10. K8s ב-DevOps

- מאפשר **CI/CD** pipelines, תומך **GitOps** (Git כמקור-אמת לפריסות).
- מתקנן deployments בין סביבות, מניע פלטפורמות cloud-native.

> **ב-ULease:** ה-CI החוסם-merge כבר קיים (D-023). GitOps (Argo CD — `CLOUD_ARCHITECT_SKILLS` §4) הוא יעד V1+, לא MVP.

---

## §11. ההכרעה ל-ULease: מתי (ואם) K8s 🎯

| שיקול | docker-compose (MVP — הקיים) | Kubernetes (V1+/scale) |
|--------|------------------------------|------------------------|
| מורכבות תפעול | נמוכה — קובץ אחד | גבוהה — קלאסטר לתחזק |
| מתאים ל- | שירות/שניים, עומס נמוך | ריבוי שירותים, autoscaling, self-healing |
| צוות | מתאים למייסד+Tech Lead בודד | דורש בגרות DevOps |
| ההמלצה | **ה-MVP נשאר על docker-compose** | מעבר כש: Ultra·Master·Max נפרדים לשירותים · עומס דורש HPA · SLA דורש self-healing מנוהל |

> **דגל אנטי-over-engineering** (תקדים `AI_PROJECT_STRUCTURE` §3.2, D-046): K8s ל-MVP של marketplace בודד הוא בדיוק ה"6 חודשים ל-MVP" ש-`ULEASE_HIRING` §ו מסמן 🔴. **שאלת design-review ל-Tech Lead:** "מה הטריגר המדיד למעבר ל-K8s?" — תשובה טובה נוקבת ב-metric (עומס/שירותים/SLA), לא ב"כי זה הסטנדרט".

---

## §12. החיבור ל-OS ולמסלול הלמידה

| איפה | מה |
|------|-----|
| `CLOUD_ARCHITECT_SKILLS.md` §4 | K8s = ה-deep-dive של תא ה-Cloud-Native (Microservices) |
| `AI_SYSTEM_DESIGN.md` | השירותים ש-K8s מתזמר (gateway · API · תורים) |
| `AI_PROJECT_STRUCTURE.md` | הריפו שנפרס; manifests חיים לצד הקוד |
| `AI_CLAUDE_STACK_2026.md` | CI/GitOps כשכבת ה-ship |
| Learn-vs-Delegate | **המייסד:** המושגים + שאלת הטריגר למעבר · **ה-Tech Lead:** המימוש (manifests, Helm, cluster ops) — תאום ל-`AI_LINEAR_ALGEBRA` (המייסד סוקר, ה-Tech Lead מיישם) |

---

## Document Control

| גרסה | שינוי | תאריך |
|------|--------|--------|
| 1.0.0 | יצירת המודול — תזמור קונטיינרים (K8s 101): הבעיה, מושגי הליבה, ארכיטקטורת Control Plane/Worker (API Server·etcd·Scheduler·kubelet·kube-proxy·CRI), Workloads, רשת, Config/Secrets, Scaling/Resilience, Observability, Security ו-DevOps — כולם ממופים ל-ULease + §11 ההכרעה מתי/אם K8s (MVP=docker-compose) ודגל אנטי-over-engineering. מבוסס אינפוגרפיקת *"Kubernetes 101"* (CloudNimbus, D-061) | 2026-06-04 |

**Attribution.** מבנה ה-K8s 101 ו-10 הסעיפים: האינפוגרפיקה *"Kubernetes 101"* (Lawal Abdullateef A. / CloudNimbus). הזיקוק, המיפוי ל-ULease והכרעת docker-compose-מול-K8s — חלק מה-Claude OS של Avraham Bar Yochai Chazan.

**Confidentiality.** קובץ זה הוא חלק מה-Claude Operating System האישי של Avraham Bar Yochai Chazan.

— *End of KUBERNETES_101.md v1.0.0 —*
