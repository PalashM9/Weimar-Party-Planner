import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <section className="hero">
      <div className="kicker">Berlin energy • Weimar nights • Open maps</div>
      <h1>Host underground parties. Discover scenes. Request entry.</h1>
      <p>
        A techno-inspired party planner where hosts create events, guests request
        access, and every venue comes alive on a live map with a dark German club aesthetic.
      </p>

      <div className="hero-actions">
        <Link to="/explore" className="button-primary">Explore parties</Link>
        <Link to="/create-party" className="button-secondary">Host a party</Link>
      </div>

      <div className="grid-3">
        <div className="panel">
          <div className="section-title">Host flow</div>
          <p>Create a party, set the date, add location, and manage entry requests.</p>
        </div>
        <div className="panel">
          <div className="section-title">Attendee flow</div>
          <p>Browse public events, inspect the vibe, and request access with a message.</p>
        </div>
        <div className="panel">
          <div className="section-title">Live city feel</div>
          <p>Show venues on a free interactive map powered by OpenStreetMap and Leaflet.</p>
        </div>
      </div>
    </section>
  );
}
