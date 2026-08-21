# Asynchronous Programming

This beginner-friendly codelab teaches how Dart handles work that finishes later, such as timers, network requests, file operations, and live updates. It uses small score-loading and restaurant-order examples so learners can understand one concept at a time before combining them.

By the end, learners will be able to use a `Future` for one later result, use a `Stream` for several updates, handle asynchronous errors, and represent loading, success, and error states commonly used in Flutter apps.

## Plan

1. Why asynchronous programming matters in Dart and Flutter
2. Synchronous versus asynchronous work using `prepareOrder()`, `Duration`, and `Future.delayed()`
3. `Future<T>` as one value or error that arrives later
4. Creating a delayed future and receiving its value with `then()`
5. Reading future-based code from top to bottom with `async` and `await`
6. Handling future errors with `try`, `catch`, and `finally`
7. Waiting for independent futures together with `Future.wait()`
8. `Stream<T>` as several values over time and consuming them with `await for`
9. Listening to a stream with `listen()`, `onError`, and `onDone`
10. Creating a simple stream with `async*` and `yield`
11. Showing loading, success, and error states while data loads
12. Practice: load one restaurant order and consume its status updates
13. Beginner knowledge check covering the essential async concepts
14. Final task: build a small asynchronous restaurant order tracker
