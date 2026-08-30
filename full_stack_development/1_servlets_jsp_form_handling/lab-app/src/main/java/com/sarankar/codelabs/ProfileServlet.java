package com.sarankar.codelabs;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(name = "ProfileServlet", urlPatterns = "/profile", loadOnStartup = 1)
public class ProfileServlet extends HttpServlet {

    @Override
    public void init() throws ServletException {
        super.init();
        getServletContext().log("ProfileServlet initialized");
    }

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws IOException {
        response.sendRedirect(request.getContextPath() + "/");
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        request.setCharacterEncoding("UTF-8");

        String name = valueOrEmpty(request.getParameter("name")).trim();
        String email = valueOrEmpty(request.getParameter("email")).trim();

        request.setAttribute("formName", name);
        request.setAttribute("formEmail", email);

        if (name.isBlank() || email.isBlank()) {
            request.setAttribute("errorMessage", "Please enter both your name and email.");
            request.getRequestDispatcher("/index.jsp").forward(request, response);
            return;
        }

        if (!isValidEmail(email)) {
            request.setAttribute("errorMessage", "Please enter an email address such as student@example.com.");
            request.getRequestDispatcher("/index.jsp").forward(request, response);
            return;
        }

        request.setAttribute("submittedName", name);
        request.setAttribute("submittedEmail", email);
        request.getRequestDispatcher("/WEB-INF/result.jsp").forward(request, response);
    }

    private String valueOrEmpty(String value) {
        return value == null ? "" : value;
    }

    private boolean isValidEmail(String email) {
        int at = email.indexOf('@');
        int dot = email.lastIndexOf('.');
        return at > 0 && dot > at + 1 && dot < email.length() - 1;
    }

    @Override
    public void destroy() {
        getServletContext().log("ProfileServlet destroyed");
        super.destroy();
    }
}
