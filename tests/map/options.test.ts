import { MapOptions } from '../../src/map/options';
import { GUID } from '../../src/utils';

import { default as setupJSDOM } from '../jsdom';
import { assert } from 'chai';

const DUMMY_PROPERTIES = {
    first: {
        values: [],
    },
    second: {
        values: [],
    },
};

const DUMMY_CALLBACK = () => {
    return { top: 0, left: 0 };
};

function traverseDOM(element: Element, callback: (element: Element) => void) {
    if (element.children) {
        const elements = element.children;
        for (let i = 0; i < elements.length; i++) {
            traverseDOM(elements[i], callback);
        }
    }
    callback(element);
}

describe('MapOptions', () => {
    before(() => {
        setupJSDOM();
    });

    it('can remove itself from DOM', () => {
        const root = document.createElement('div');
        const options = new MapOptions(
            root,
            'this-is-my-id' as GUID,
            DUMMY_PROPERTIES,
            DUMMY_CALLBACK
        );
        assert(root.innerHTML !== '');
        assert(document.body.innerHTML !== '');

        options.remove();
        assert(document.body.innerHTML === '');
        assert(root.innerHTML === '');
    });

    it('has a unique id in the page', () => {
        const root = document.createElement('div');

        const guid = 'this-is-my-id' as GUID;
        const options = new MapOptions(root, guid, DUMMY_PROPERTIES, DUMMY_CALLBACK);
        traverseDOM(document.body, (element) => {
            if (element.id) {
                assert(element.id.includes(guid));
            }
        });

        options.remove();
    });
});
