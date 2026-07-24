import { BarChart3, BrainCircuit, Map, Target } from 'lucide-react';
import type { ReactNode } from 'react';

const navItems = [
  { id: 'overview', label: 'Overview', icon: BarChart3 },
  { id: 'map', label: 'Map', icon: Map },
  { id: 'prediction', label: 'Prediction', icon: Target },
  { id: 'explainability', label: 'Explainability', icon: BrainCircuit }
];

interface ShellProps {
  activePage: string;
  onPageChange: (page: string) => void;
  children: ReactNode;
}

export function Shell({ activePage, onPageChange, children }: ShellProps) {
  return (
    <div className="min-h-screen bg-slate-50 text-ink">
      <aside className="fixed inset-y-0 left-0 z-10 hidden w-72 border-r border-line bg-white px-5 py-6 lg:block">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-muted">Analytics</p>
          <h1 className="mt-2 text-2xl font-semibold leading-tight">Crime Risk Dashboard</h1>
        </div>
        <nav className="mt-10 space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const active = activePage === item.id;
            return (
              <button
                key={item.id}
                className={`flex w-full items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition ${
                  active ? 'bg-slate-900 text-white' : 'text-muted hover:bg-slate-100 hover:text-ink'
                }`}
                onClick={() => onPageChange(item.id)}
                type="button"
              >
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </nav>
        <div className="absolute bottom-6 left-5 right-5 rounded-md border border-line bg-slate-50 p-4 text-sm text-muted">
          State-wise NCRB-style forecasting using lag features, population, literacy, urbanization, and SHAP importance.
        </div>
      </aside>

      <main className="lg:pl-72">
        <div className="sticky top-0 z-20 border-b border-line bg-white/95 px-4 py-3 backdrop-blur lg:hidden">
          <div className="flex gap-2 overflow-x-auto">
            {navItems.map((item) => (
              <button
                key={item.id}
                className={`shrink-0 rounded-md px-3 py-2 text-sm font-medium ${
                  activePage === item.id ? 'bg-slate-900 text-white' : 'bg-slate-100 text-muted'
                }`}
                onClick={() => onPageChange(item.id)}
                type="button"
              >
                {item.label}
              </button>
            ))}
          </div>
        </div>
        <div className="mx-auto max-w-7xl px-4 py-6 sm:px-6 lg:px-8">{children}</div>
      </main>
    </div>
  );
}

