import { Routes, Route } from "react-router-dom";
import AppLayout from "./layout/AppLayout";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import DashboardPage from "./pages/DashboardPage";
import CreatePartyPage from "./pages/CreatePartyPage";
import ExplorePage from "./pages/ExplorePage";
import PartyDetailPage from "./pages/PartyDetailPage";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<AppLayout />}>
        <Route index element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/create-party" element={<CreatePartyPage />} />
        <Route path="/explore" element={<ExplorePage />} />
        <Route path="/parties/:id" element={<PartyDetailPage />} />
      </Route>
    </Routes>
  );
}
