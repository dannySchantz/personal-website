export default function NotFound() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <p className="font-mono text-xs uppercase tracking-[0.22em] text-muted">404</p>
      <h1 className="mt-4 text-3xl font-semibold tracking-tight">
        This page isn&rsquo;t on the CV.
      </h1>
      <p className="mt-4 max-w-sm text-ink-soft">
        The address may have changed. Everything worth finding is one link away.
      </p>
      <a
        href="/"
        className="prose-link mt-8 font-mono text-sm"
      >
        Back to the homepage
      </a>
    </main>
  );
}
