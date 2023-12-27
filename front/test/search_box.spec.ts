import { mount } from "@vue/test-utils";
import { expect, test, describe } from 'vitest'
import SearchBox from '../src/components/SearchBox.vue'

test('should work as expected', () => {
    expect(Math.sqrt(4)).toBe(2)
})

describe("SearchBox.vue", () => {
    test("renders the correct style for error", () => {
        const wrapper = mount(SearchBox)
        console.log(wrapper)
    });
});