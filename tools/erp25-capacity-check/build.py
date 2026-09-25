from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
BUILDER = ROOT / "_builder"
sys.path.insert(0, str(BUILDER))

from src.services.epf_factory import EpfFactory

bsl = (ROOT / "form_module.bsl").read_text(encoding="utf-8")
form_spec = json.loads((ROOT / "form_spec.json").read_text(encoding="utf-8"))
out = ROOT / "dist" / "ПроверкаВыполнимостиПлана_ERP_2_5_22_186.epf"
out.parent.mkdir(parents=True, exist_ok=True)

factory = EpfFactory()
result = factory.create_epf(
    name="ПроверкаВыполнимостиПланаERP",
    synonym="Проверка выполнимости плана производства ERP 2.5.22.186",
    bsl_code=bsl,
    output_epf=out,
    form_spec=form_spec,
    save_sources=True,
    skip_bsl_validation=True,
)

print(json.dumps({
    "ok": result.ok,
    "error": result.error,
    "epf_path": str(result.epf_path) if result.epf_path else None,
    "size_bytes": result.size_bytes,
    "round_trip_ok": result.round_trip_ok,
    "bsl_lines": result.bsl_lines,
}, ensure_ascii=False, indent=2))

if not result.ok or not result.round_trip_ok:
    raise SystemExit(1)
