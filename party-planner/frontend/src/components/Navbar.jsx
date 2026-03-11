import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <header className="nav">
      <div className="brand">
        <span className="brand-mark">▣</span>
        <span>Weimar Nacht</span>
      </div>

      <nav className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/explore">Explore</Link>
        <Link to="/create-party">Host</Link>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/login" className="nav-button">Login</Link>
      </nav>
    </header>
  );
}
