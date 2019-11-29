import {ScatterPlot} from "./plot";
import {StructureViewer} from "./viewer";
import {EnvironementSlider} from './slider';
import {PropertiesTable} from './properties';

require('./static/sketchviz.css');

interface VizualizerData {
    name: string;
    properties: {
        [name: string]: string[] | number[];
    };
    structures: string[];
}

function checkData(o: any) {
    if (!('name' in o && typeof o['name'] === 'string')) {
        throw Error("missing 'name' in Sketchviz.input");
    }

    if (!('properties' in o && typeof o['properties'] === 'object')) {
        throw Error("missing 'properties' in Sketchviz.input");
    }
    for (const key in o['properties']) {
        if (o['properties'][key].length === undefined ||
            !(typeof o['properties'][key][0] === 'string' ||
              typeof o['properties'][key][0] === 'number')) {
                  throw Error("wrong type for 'properties' in Sketchviz.input");
              }
    }

    if (!('structures' in o && o['structures'].length !== undefined && typeof o['structures'][0] === 'string')) {
        throw Error("missing 'structures' in Sketchviz.input");
    }

    // Check that properties and structures have the same size
    const size = o['structures'].length;
    for (const key in o['properties']) {
        if (o['properties'][key].length !== size) {
            throw Error("properties and structures don't have the same size")
        }
    }
}

interface VizualizerInput extends VizualizerData {
    plotId: string;
    viewerId: string;
    j2sPath: string;
    sliderId: string;
    propertiesId: string;
}

function checkInput(o: any) {
    checkData(o);

    if (!('plotId' in o && typeof o['plotId'] === 'string')) {
        throw Error("missing 'plotId' in Sketchviz.input");
    }

    if (!('viewerId' in o && typeof o['viewerId'] === 'string')) {
        throw Error("missing 'viewerId' in Sketchviz.input");
    }

    if (!('j2sPath' in o && typeof o['j2sPath'] === 'string')) {
        throw Error("missing 'j2sPath' in Sketchviz.input");
    }

    if (!('sliderId' in o && typeof o['sliderId'] === 'string')) {
        throw Error("missing 'sliderId' in Sketchviz.input");
    }

    if (!('propertiesId' in o && typeof o['propertiesId'] === 'string')) {
        throw Error("missing 'propertiesId' in Sketchviz.input");
    }
}


class Vizualizer {
    public viewer: StructureViewer;
    public plot: ScatterPlot;
    public slider: EnvironementSlider;
    public table: PropertiesTable;
    private _ids: {
        plot: string;
        viewer: string;
        slider: string;
        table: string;
    }

    constructor(input: VizualizerInput) {
        checkInput(input);

        this._ids = {
            plot: input.plotId,
            viewer: input.viewerId,
            slider: input.sliderId,
            table: input.propertiesId,
        }

        this.plot = new ScatterPlot(input.plotId, input.name, input.properties);
        this.viewer = new StructureViewer(input.viewerId, input.j2sPath, input.structures);
        this.slider = new EnvironementSlider(input.sliderId, input.structures.length - 1);
        this.table = new PropertiesTable(input.propertiesId, input.properties);
        this.plot.onSelectedUpdate((i) => {
            this.slider.changed(i);
            this.viewer.showStructure(i);
            this.table.display(i);
        });
        this.slider.onChange((i) => this.plot.select(i));
    }

    public changeDataset(data: VizualizerData) {
        checkData(data);

        this.plot.changeDataset(data.name, data.properties);
        this.viewer.changeDataset(data.structures);
        this.slider.changeDataset(data.structures.length - 1);
        this.table = new PropertiesTable(this._ids.table, data.properties);
    }
}

export {
    StructureViewer,
    ScatterPlot,
    EnvironementSlider,
    PropertiesTable,
    Vizualizer,
};
