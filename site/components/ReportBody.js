export default function ReportBody({ htmlContent }) {
  return (
    <div className="report-fade-in">
      <div
        className="report-html"
        dangerouslySetInnerHTML={{ __html: htmlContent }}
      />
    </div>
  )
}
