import React, {useState} from "react";
import {Panel, SelectPicker} from "rsuite";

interface Model {
    id: number,
    name: string,
    description: string
}

interface SelectModelProps {
    models: Model[]
}

const SelectModel = ({models}: SelectModelProps) => {
    const [selectedModel, setSelectedModel] = useState<string | null>(null);

    return (
        <Panel shaded header={'Выберите область анализа'}>
            <SelectPicker value={selectedModel}
                          data={models.map(m => ({
                              label: m.name,
                              value: m.id
                          }))}
                          onChange={v => setSelectedModel(v)}
            />
        </Panel>
    );
}

export default SelectModel;