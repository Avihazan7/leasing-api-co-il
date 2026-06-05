# Authentication vs Authorization — Complete Guide for Beginners

> A plain transcription of the M-SoftTech infographic.

---

## 1. What is Authentication?

**Authentication verifies the identity of a user.**

> "Are you really who you claim to be?"

Login form fields: Email or Username, Password, **LOGIN**.

**Real-Life Example — ATM Machine**
1. Insert Card
2. Enter PIN

Bank verifies: Card + PIN = Valid? → If valid: **Authenticated** ✅

## 2. What is Authorization?

**Authorization determines what an authenticated user is allowed to do.**

> "What can you do?"

**ADMIN**
- ✓ Create Users
- ✓ Delete Users
- ✓ Update Users
- ✓ View Reports

**USER**
- ✓ View Profile
- ✗ Delete Users
- ✗ Manage System

**Real-Life Example — Airport Access**
- **Authentication:** Passport Verification
- **Authorization:** Business Class? VIP Lounge? Staff Access?
- Different permissions for different people.

## Authentication vs Authorization

| | Authentication | Authorization |
|---|---|---|
| **Answers** | Who are you? | What can you do? |
| **Purpose** | Identity Verification | Permission Verification |
| **When** | Happens First | Happens After Authentication |
| **Example** | Login, Password, OTP | Roles, Permissions, Access Control |
| **Failure Code** | 401 Unauthorized | 403 Forbidden |

**Quick Memory Trick**
- **Authentication** → Who Are You?
- **Authorization** → What Can You Do?
- Authentication first, Authorization second.

## 3. Authentication Flow

User → Login → Verify Credentials → Authenticated → Generate Token → Access Application

**Request (Login):**
```
POST /login
{
  "email": "john@gmail.com",
  "password": "123456"
}
```

**Response (Token):**
```
{
  "token": "abc123xyz",
  "tokenType": "Bearer"
}
```

## 4. Authorization Flow

User Request → Token Verification → Check Role/Permission → Allow / Deny Access

**Request Example:** `DELETE /users/1`

Check Role = Admin?
- **Yes** → 200 OK
- **No** → 403 Forbidden

## 5. Types of Authentication

1. **Password-Based Authentication** — Email + Password. Most common method.
2. **Multi-Factor Authentication (MFA)** — Password + OTP / Code. Extra layer of security.
3. **Biometric Authentication** — Fingerprint, Face ID, Retina Scan. Hard to steal, user-friendly.
4. **Social Login** — Login with Google, GitHub, Facebook, etc. Faster signup and better UX.

## 6. Types of Authorization

1. **Role-Based Access Control (RBAC)** — Access based on user roles. Example: Admin, Manager, User.
2. **Permission-Based Access Control** — Access based on specific permissions. Example: `read_users`, `create_users`.
3. **Attribute-Based Access Control (ABAC)** — Access based on attributes and conditions. Example: Department = HR, Location = India, Time = Working Hours.

## 7. Session-Based Authentication

Traditional method using server-side sessions.
- Login
- Server Creates Session
- Session ID Stored
- Browser Cookie

**Example Cookie:** `session_id = abc123`

Server remembers the user.

## 8. Token-Based Authentication (JWT)

Modern and stateless authentication.
- Login
- Generate JWT Token
- Client Stores Token
- Token Sent With Requests
- Server Verifies Token
- Access Granted

**JWT Structure:** Header . Payload . Signature → `xxxxx.yyyyy.zzzzz`

**JWT Payload Example:**
```
{
  "id": 1,
  "name": "John",
  "role": "Admin",
  "iat": 1716087000,
  "exp": 1716090600
}
```

## 9. HTTP Status Codes

**401 Unauthorized**
- Not logged in
- Invalid token
- Expired token
- Authentication failed

**403 Forbidden**
- Logged in
- But no permission
- Access denied

## 10. Best Practices

**Authentication Best Practices**
- ✓ Hash passwords using bcrypt
- ✓ Use HTTPS everywhere
- ✓ Enable Multi-Factor Authentication
- ✓ Use strong password policies
- ✓ Set token expiration
- ✓ Secure cookies (HttpOnly, Secure)

**Authorization Best Practices**
- ✓ Use RBAC (Role-Based Access Control)
- ✓ Validate every request
- ✓ Never trust client-side roles
- ✓ Apply least privilege principle
- ✓ Log security events
- ✓ Regular permission audits

## 11. Real-World Example

**Customer (User)**
- ✓ View Products
- ✓ Add To Cart
- ✓ Place Orders
- ✗ Delete Products
- ✗ Manage Users

**Admin**
- ✓ Add Products
- ✓ Update Products
- ✓ Delete Products
- ✓ Manage Users
- ✓ View Reports

---

**Bottom flow:** Authentication → JWT Created → Request Delete Product → Authorization → Authorization Check → Allow / Deny

*Secure your application. Authenticate first, authorize second!*
