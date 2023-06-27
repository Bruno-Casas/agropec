import type { Category } from "./Category";
import type { Earring } from "./Earring";

export class Bovine {
    id: number | null | undefined;
    sex: number | null | undefined;
    weight: number | null | undefined;
    category: Category | null | undefined;
    earring: Earring | null | undefined;
}
