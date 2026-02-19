import { describe, it, expect } from "vitest";
import { mountSuspended } from "@nuxt/test-utils/runtime";
import NewsPage from "~/pages/news.vue";

describe("News Page", () => {
  it("renders the heading", async () => {
    const component = await mountSuspended(NewsPage);
    expect(component.find("h1").text()).toBe("News");
  });
});
