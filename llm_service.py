

import google.generativeai as genai
from app.core import config
from app.core.logger import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        """
        Khởi tạo và cấu hình API Gemini.
        """
        logger.info("Bắt đầu cấu hình dịch vụ Gemini...")
        try:
            # Cấu hình API key
            genai.configure(api_key=config.GEMINI_API_KEY)
            
            # Chọn model, gemini-1.5-flash là model mới, rất nhanh và hiệu quả
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            logger.info("Cấu hình dịch vụ Gemini thành công. Model: gemini-1.5-flash.")
            
        except Exception as e:
            logger.error(f"LỖI NGHIÊM TRỌNG KHI CẤU HÌNH GEMINI: {e}", exc_info=True)
            # Kiểm tra xem có phải do thiếu API key không
            if "API key not valid" in str(e) or not config.GEMINI_API_KEY:
                logger.error("Vui lòng kiểm tra lại GEMINI_API_KEY trong file app/core/config.py.")
            raise

    def generate_response(self, question: str, context: list[str]) -> str:
        """
        Tạo câu trả lời từ Gemini dựa trên câu hỏi và ngữ cảnh RAG.
        """
        context_str = "\n".join(context)
        
        # Tạo prompt tối ưu cho Gemini
        prompt = (
            "Bạn là một trợ lý ảo thông minh và thân thiện, nói tiếng Việt."
            "Dựa vào thông tin trong phần 'Ngữ cảnh' dưới đây để trả lời 'Câu hỏi' của người dùng một cách chính xác và chi tiết."
            "Nếu thông tin không có trong ngữ cảnh, hãy lịch sự trả lời rằng bạn không có thông tin về vấn đề đó.\n\n"
            "--- Ngữ cảnh ---\n"
            f"{context_str}\n\n"
            "--- Câu hỏi ---\n"
            f"{question}\n\n"
            "--- Trả lời ---\n"
        )
        
        logger.info("Gửi yêu cầu đến API Gemini...")
        try:
            # Gọi API và lấy kết quả
            response = self.model.generate_content(prompt)
            
            ai_response_text = response.text
            logger.info("Đã nhận phản hồi từ Gemini thành công.")
            return ai_response_text
            
        except Exception as e:
            logger.error(f"Lỗi khi gọi API Gemini: {e}", exc_info=True)
            return "Xin lỗi, tôi đang gặp sự cố khi kết nối đến dịch vụ AI. Vui lòng thử lại sau."

# Khởi tạo một instance duy nhất để toàn bộ ứng dụng sử dụng
llm_service = LLMService()