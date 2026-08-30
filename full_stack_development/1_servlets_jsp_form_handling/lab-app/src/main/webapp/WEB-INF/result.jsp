<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Submitted Profile</title>
  <link rel="stylesheet" href="${pageContext.request.contextPath}/css/styles.css">
</head>
<body>
  <main class="form-card result-card">
    <p class="eyebrow">Submission received</p>
    <h1>Hello, <c:out value="${submittedName}" />!</h1>
    <p>Your form travelled through the Servlet and reached this JSP page.</p>

    <dl>
      <div>
        <dt>Name</dt>
        <dd><c:out value="${submittedName}" /></dd>
      </div>
      <div>
        <dt>Email</dt>
        <dd><c:out value="${submittedEmail}" /></dd>
      </div>
    </dl>

    <a class="button-link" href="${pageContext.request.contextPath}/">Submit another profile</a>
  </main>
</body>
</html>
