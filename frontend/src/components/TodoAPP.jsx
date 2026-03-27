import { useState, useEffect } from "react";

export default function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");

  const fetchTodos = async () => {
    const res = await fetch("http://localhost:8000/todos");
    const data = await res.json();
    setTodos(data);
  };

  const addTodo = async () => {
    if (!title) return;
    await fetch("http://localhost:8000/todos", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title, description, completed: false }),
    });
    setTitle("");
    setDescription("");
    fetchTodos();
  };

  const toggleTodo = async (id, completed) => {
    await fetch(`http://localhost:8000/todos/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ completed: !completed }),
    });
    fetchTodos();
  };

  const deleteTodo = async (id) => {
    await fetch(`http://localhost:8000/todos/${id}`, { method: "DELETE" });
    fetchTodos();
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", textAlign: "center" }}>
      <h1>📝 Todo List</h1>
      <input
        placeholder="タイトル"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        placeholder="詳細"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        style={{ marginLeft: "10px" }}
      />
      <button onClick={addTodo} style={{ marginLeft: "10px" }}>
        追加
      </button>

      <ul style={{ listStyle: "none", padding: 0 }}>
        {todos.map((todo) => (
          <li
            key={todo.id}
            style={{
              margin: "10px 0",
              textDecoration: todo.completed ? "line-through" : "none",
            }}
          >
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id, todo.completed)}
            />
            {todo.title} — {todo.description}
            <button onClick={() => deleteTodo(todo.id)} style={{ marginLeft: "10px" }}>
              🗑️
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
