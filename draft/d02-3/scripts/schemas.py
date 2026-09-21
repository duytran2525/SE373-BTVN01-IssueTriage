"""Pydantic schemas and application-side validation rules (R3, R4)."""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

Component = Literal["payment", "identity", "search"]
Severity = Literal["P0", "P1", "P2", "P3"]
Status = Literal["classified", "insufficient_data", "out_of_scope"]


class IssueTriage(BaseModel):
    """The machine-readable contract between this application and the LLM."""

    model_config = ConfigDict(extra="forbid")

    status: Status = Field(
        description="classified nếu là issue phần mềm hợp lệ; insufficient_data nếu thiếu thông tin; out_of_scope nếu không liên quan."
    )
    severity: Severity | None = Field(
        default=None,
        description="Mức độ nghiêm trọng P0/P1/P2/P3. Bắt buộc có nếu status='classified'.",
    )
    component: Component | None = Field(
        default=None,
        description="Phân hệ chịu trách nhiệm: payment, identity hoặc search. Bắt buộc có nếu status='classified'.",
    )
    needs_urgent_response: bool = Field(
        default=False,
        description="Đánh dấu cần can thiệp khẩn cấp ngay lập tức.",
    )
    reason: str = Field(
        description="Giải thích ngắn gọn căn cứ xác định mức độ nghiêm trọng và phân hệ."
    )

    @model_validator(mode="after")
    def validate_application_invariants(self) -> IssueTriage:
        """Application-side semantic verification (Defense-in-depth).
        
        Even if the provider produces syntactically valid JSON according to schema,
        domain business rules and cross-field invariants must be verified by the application.
        """
        # Invariant 1: Non-empty semantic explanation
        if not self.reason or not self.reason.strip():
            raise ValueError("Lỗi validation application: Trường 'reason' không được để trống.")

        # Invariant 2: P0 requires immediate escalation / urgent response
        if self.severity == "P0" and not self.needs_urgent_response:
            raise ValueError(
                "Lỗi bất biến liên trường (cross-field invariant): "
                "Khi severity='P0', needs_urgent_response bắt buộc phải là True."
            )

        # Invariant 3: Classified status requires component and severity
        if self.status == "classified":
            if self.severity is None:
                raise ValueError("Lỗi validation: Khi status='classified', 'severity' không được là null.")
            if self.component is None:
                raise ValueError("Lỗi validation: Khi status='classified', 'component' không được là null.")

        return self
