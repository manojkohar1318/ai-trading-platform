import {describe,it,expect} from 'vitest'; import {stocks} from '../demo';
describe('demo universe',()=>{it('is non-empty and scored',()=>{expect(stocks.length).toBeGreaterThan(0); expect(stocks[0][3]).toBeGreaterThanOrEqual(0)})})
