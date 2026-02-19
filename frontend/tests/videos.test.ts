import { describe, it, expect } from "vitest";
import { mountSuspended } from "@nuxt/test-utils/runtime";
import VideosPage from "~/pages/videos.vue";

describe("Videos Page", () => {
  it("renders the heading", async () => {
    const component = await mountSuspended(VideosPage);
    expect(component.find("h1").text()).toBe("Videos");
  });
});
