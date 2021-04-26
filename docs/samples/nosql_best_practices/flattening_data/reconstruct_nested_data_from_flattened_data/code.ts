export interface RetrievedLayoutItemData {
    active?: boolean;
    size?: boolean;
    parentId?: string;
}

export interface ClientLayoutItemData {
    active?: boolean;
    size?: boolean;
    children?: { [key: string]: ClientLayoutItemData };
}

export function reconstructData(flattenedData: { [key: string]: RetrievedLayoutItemData }): ClientLayoutItemData[] {
    const rootItems: ClientLayoutItemData[] = [];
    const allItems: { [key: string]: ClientLayoutItemData } = {};
    const childrenWaitingByParentIds: { [key: string]: { [key: string]: ClientLayoutItemData } } = {};

    for (let itemKeyId in flattenedData) {
        const retrievedItemData: RetrievedLayoutItemData = flattenedData[itemKeyId];
        const parentId: string | undefined = retrievedItemData.parentId;

        const clientItemData: ClientLayoutItemData = {
            active: retrievedItemData.active, size: retrievedItemData.size
        };
        allItems[itemKeyId] = clientItemData;

        if (parentId === undefined) {
            rootItems.push(clientItemData);
        } else {
            if (!(childrenWaitingByParentIds.hasOwnProperty(parentId))) {
                childrenWaitingByParentIds[parentId] = {};
            }
            childrenWaitingByParentIds[parentId][itemKeyId] = clientItemData;
        }
    }

    for (let parentKeyId in childrenWaitingByParentIds) {
        const childrenItems = childrenWaitingByParentIds[parentKeyId];
        allItems[parentKeyId].children = childrenItems;
    }
    return rootItems;
}
const reconstructedRootItems = reconstructData(flattenedDataYouRetrievedFromYourBackend);
console.log(reconstructedRootItems);