import { describe, it, expect } from "vitest";
import { mountSuspended } from "@nuxt/test-utils/runtime";
import LearnPage from "~/pages/learn.vue";

describe("Learn Page", () => {
  it("renders the heading", async () => {
    const component = await mountSuspended(LearnPage);
    expect(component.find("h1").text()).toBe("Learn");
  });
});
