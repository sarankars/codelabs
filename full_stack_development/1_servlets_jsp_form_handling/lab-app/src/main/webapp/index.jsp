<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ taglib prefix="c" uri="jakarta.tags.core" %>
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Student Profile Form</title>
  <link rel="stylesheet" href="${pageContext.request.contextPath}/css/styles.css">
</head>
<body>
  <main class="form-card">
    <p class="eyebrow">Servlet + JSP Lab</p>
    <h1>Tell us about yourself</h1>
    <p class="intro">Submit the form to send your details to a Java Servlet.</p>

    <c:if test="${not empty errorMessage}">
      <div class="error" role="alert"><c:out value="${errorMessage}" /></div>
    </c:if>

    <form action="${pageContext.request.contextPath}/profile" method="post">
      <label for="name">Name</label>
      <input id="name" name="name" type="text" value="<c:out value='${formName}' />"
             autocomplete="name" required>

      <label for="email">Email</label>
      <input id="email" name="email" type="email" value="<c:out value='${formEmail}' />"
             autocomplete="email" required>

      <button type="submit">Submit profile</button>
    </form>
  </main>
</body>
</html>
