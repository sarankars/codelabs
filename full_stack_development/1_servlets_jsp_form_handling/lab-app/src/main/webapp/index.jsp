<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Student Form</title>
</head>
<body>
  <h1>Student Form</h1>
  <form action="${pageContext.request.contextPath}/submit" method="post">
    <p>
      <label for="name">Name:</label>
      <input id="name" name="name" type="text" required>
    </p>
    <p>
      <label for="email">Email:</label>
      <input id="email" name="email" type="email" required>
    </p>
    <button type="submit">Submit</button>
  </form>
</body>
</html>
