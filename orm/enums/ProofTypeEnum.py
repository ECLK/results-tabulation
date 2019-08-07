import enum


class ProofTypeEnum(enum.Enum):
    Invoice = 1
    InvoiceStationaryItemReceive = 2
    ManuallyFilledTallySheets = 3
    ManuallyFilledReports = 4

