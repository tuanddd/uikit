import type { ReactNode } from "react";

/**
 * FlowShell — renders one flow definition and the screens per step.
 * Reference for the React stack; Svelte and Astro follow the same props and section order.
 * A dev surface: never linked, gated out of production (see the design-system viewer).
 */

type Step = {
  id: string;
  n: number;
  title: string;
  state?: string;
  route?: string;
  restsOn?: string;
  linkedTo: string | null;
};
type Why = { decision: string; restsOn: string; confidence: "reference" | "principle" };
type ComponentRow = { name: string; class: string; from: string; steps: string };
type LedgerRow = {
  name: string;
  class: string;
  kind: string;
  nearest: string;
  why: string;
  proposal: string;
  status: string;
};

export type FlowDef = {
  feature: string;
  slug: string;
  group: string;
  drawnOn: string;
  frameWidth: number;
  requirement: { text: string; source: string };
  steps: Step[];
  why: Why[];
  components: ComponentRow[];
  ledger: LedgerRow[];
};

export type FlowLink = { slug: string; feature: string };

export function FlowShell({
  def,
  screens,
  prev,
  next,
}: {
  def: FlowDef;
  screens: Record<string, ReactNode>;
  prev?: FlowLink;
  next?: FlowLink;
}) {
  return (
    <div className="uikit-flow">
      <style>{styles}</style>

      <header className="uikit-flow__head">
        <h1>{def.feature}</h1>
        <p className="uikit-flow__meta">
          {def.group} · {def.steps.length} steps · frame {def.frameWidth}px · Static, mock values
        </p>
        <figure className="uikit-flow__road">
          <blockquote>{def.requirement.text}</blockquote>
          <figcaption>{def.requirement.source}</figcaption>
        </figure>
      </header>

      <nav className="uikit-flow__bar">
        <a href="/uikit/flows">All flows</a>
        <a href="#flow">The flow</a>
        <a href="#why">Why it looks like this</a>
        <a href="#build">Building on it</a>
      </nav>

      <section id="flow">
        <h2>The flow</h2>
        <ol className="uikit-flow__steps">
          {def.steps.map((step) =>
            step.linkedTo ? (
              <li key={step.id} id={step.id}>
                <span className="uikit-flow__num">{step.n}</span>
                <a href={step.linkedTo}>{step.title} — drawn in another flow</a>
              </li>
            ) : (
              <li key={step.id} id={step.id}>
                <span className="uikit-flow__num">{step.n}</span>
                <a href={`#${step.id}`}>{step.title}</a>
                {step.state && <span className="uikit-flow__state">{step.state}</span>}
                {step.route && <code>{step.route}</code>}
              </li>
            ),
          )}
        </ol>
      </section>

      <section id="steps">
        {def.steps
          .filter((step) => !step.linkedTo)
          .map((step) => (
            <article key={step.id} className="uikit-flow__board" id={`${step.id}-board`}>
              <div className="uikit-flow__bh">
                <span className="uikit-flow__num">{step.n}</span>
                <h3>{step.title}</h3>
                {step.state && <span className="uikit-flow__state">{step.state}</span>}
                {step.route && <code>{step.route}</code>}
              </div>
              {step.restsOn && <p className="uikit-flow__why"><b>Rests on</b> {step.restsOn}</p>}
              <div className="uikit-flow__stage" style={{ maxWidth: def.frameWidth }}>
                {screens[step.id] ?? <p>Missing screen for {step.id}</p>}
              </div>
            </article>
          ))}
      </section>

      <section id="why">
        <h2>Why it looks like this</h2>
        <table>
          <thead>
            <tr><th>Decision</th><th>Rests on</th><th>Confidence</th></tr>
          </thead>
          <tbody>
            {def.why.map((row, i) => (
              <tr key={i}>
                <td>{row.decision}</td>
                <td>{row.restsOn}</td>
                <td>{row.confidence === "reference" ? "reference" : "principle, not reference"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section id="build">
        <h2>Building on it</h2>
        <h3>Components</h3>
        <table>
          <thead>
            <tr><th>Component</th><th>Class</th><th>From</th><th>Steps</th></tr>
          </thead>
          <tbody>
            {def.components.map((row, i) => (
              <tr key={i}>
                <td>{row.name}</td>
                <td><code>{row.class}</code></td>
                <td>{row.from}</td>
                <td>{row.steps}</td>
              </tr>
            ))}
          </tbody>
        </table>

        <h3>Drift from the design system</h3>
        {def.ledger.length === 0 ? (
          <p>No drift. Every component on these screens is in the design system.</p>
        ) : (
          <table>
            <thead>
              <tr><th>Drift</th><th>Kind</th><th>Nearest in the system</th><th>Why it departs</th><th>Proposal</th><th>Status</th></tr>
            </thead>
            <tbody>
              {def.ledger.map((row, i) => (
                <tr key={i}>
                  <td>{row.name} <code>{row.class}</code></td>
                  <td>{row.kind}</td>
                  <td>{row.nearest}</td>
                  <td>{row.why}</td>
                  <td>{row.proposal}</td>
                  <td>{row.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <nav className="uikit-flow__pager">
        {prev && <a href={`/uikit/flows/${prev.slug}`}>← {prev.feature}</a>}
        {next && <a href={`/uikit/flows/${next.slug}`}>{next.feature} →</a>}
      </nav>

      <p className="uikit-flow__foot">
        Part of <code>docs/flows</code> · drawn {def.drawnOn} · the live design system is{" "}
        <code>/uikit/design-system</code>
      </p>
    </div>
  );
}

const styles = `
  .uikit-flow { max-width: 1200px; margin: 0 auto; padding: var(--space-12) var(--space-8);
                color: var(--foreground); background: var(--background); font-family: var(--font-body); }
  .uikit-flow h1 { font-family: var(--font-display); font-weight: 400; }
  .uikit-flow h2 { font-family: var(--font-display); font-size: 30px; font-weight: 400;
                   margin: var(--space-12) 0 var(--space-6); }
  .uikit-flow__meta { color: var(--muted-foreground); font-size: 14px; }
  .uikit-flow__road { border-left: 4px solid var(--border); padding-left: var(--space-4); }
  .uikit-flow__bar { display: flex; flex-wrap: wrap; gap: var(--space-4); padding: var(--space-4) 0;
                     border-block: 1px solid var(--border); margin-block: var(--space-8); }
  .uikit-flow__bar a, .uikit-flow__pager a { color: var(--muted-foreground); text-decoration: none; }
  .uikit-flow__steps { display: grid; gap: var(--space-2); list-style: none; padding: 0; }
  .uikit-flow__steps li { display: flex; align-items: baseline; gap: var(--space-3); }
  .uikit-flow__num { font-variant-numeric: tabular-nums; color: var(--muted-foreground); }
  .uikit-flow__state { font-size: 12px; font-weight: 500; text-transform: uppercase;
                       color: var(--muted-foreground); }
  .uikit-flow__board { margin-block: var(--space-12); }
  .uikit-flow__bh { display: flex; align-items: baseline; gap: var(--space-3); }
  .uikit-flow__why { font-size: 14px; color: var(--muted-foreground); }
  .uikit-flow__stage { background: var(--secondary); border-radius: var(--radius-lg);
                       box-shadow: var(--shadow-border); padding: var(--space-8); overflow: auto; }
  .uikit-flow table { border-collapse: collapse; width: 100%; font-size: 14px; }
  .uikit-flow th { text-align: left; text-transform: uppercase; font-size: 11px;
                   letter-spacing: .08em; color: var(--muted-foreground); padding: var(--space-2); }
  .uikit-flow td { padding: var(--space-3) var(--space-2); border-top: 1px solid var(--border);
                   vertical-align: top; }
  .uikit-flow__pager { display: flex; justify-content: space-between; margin-block: var(--space-12); }
  .uikit-flow__foot { color: var(--muted-foreground); font-size: 13px; }
`;
