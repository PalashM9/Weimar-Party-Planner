import { Outlet } from "react-router-dom";
import Navbar from "../components/Navbar";

export default function AppLayout() {
  return (
    <div className="app-shell">
      <div className="bg-grid"></div>
      <Navbar />
      <main className="page-wrap">
        <Outlet />
      </main>
    </div>
  );
}
