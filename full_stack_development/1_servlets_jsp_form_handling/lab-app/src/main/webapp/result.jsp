<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Submitted Details</title>
</head>
<body>
  <h1>Submitted Details</h1>
  <p>Name: ${name}</p>
  <p>Email: ${email}</p>
  <a href="${pageContext.request.contextPath}/">Back to the form</a>
</body>
</html>
