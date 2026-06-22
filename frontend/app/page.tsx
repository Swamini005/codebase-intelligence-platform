import { redirect } from "next/navigation";

export default function RootPage() {
  // Redirect root path directly to dashboard
  redirect("/dashboard");
}
