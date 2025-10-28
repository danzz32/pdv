import "./App.css";
import { Suspense, lazy } from "react";
import Home from "@/pages/delivery/Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

const AdminDashboard = lazy(() => import("@/pages/pdv/Dashboard"));

function LoadingFallback() {
  return (
    <div className="flex min-h-screen w-full items-center justify-center">
      <p>Carregando...</p>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Suspense fallback={<LoadingFallback />}>
        <Routes>
          <Route index element={<Home />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </Suspense>
    </Router>
  );
}

export default App;
