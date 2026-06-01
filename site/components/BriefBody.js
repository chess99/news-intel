export default function BriefBody({ htmlContent }) {
  return (
    <div className="brief-fade-in">
      <div
        className="brief-html"
        dangerouslySetInnerHTML={{ __html: htmlContent }}
      />
    </div>
  )
}
